# app.py (simple, sin fallback)
import argparse, os, json
from pathlib import Path
from rag.retriever import RAGRetriever
import tomllib
from openai import OpenAI

rag = RAGRetriever(k=4)

SETTINGS = tomllib.loads(Path("settings.toml").read_text(encoding="utf-8"))
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "ollama"),                
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")  
)

DATA = Path(__file__).parent

def _load_json(p): 
    return json.loads(Path(p).read_text(encoding="utf-8"))

def _load_policy(): 
    return (DATA / "returns_policy.md").read_text(encoding="utf-8")

def _order_context(trk: str) -> str:
    orders = _load_json(DATA / "orders.json")
    o = next((x for x in orders if x["tracking"] == trk), None)
    if not o:
        return f"[ORDERS]\nNo existe el tracking {trk}."
    return "\n".join([
        "[ORDERS]",
        f"tracking={o['tracking']}",
        f"status={o['status']}",
        f"eta={o['eta']}",
        f"carrier={o['carrier']}",
        f"tracking_url={o['tracking_url']}",
        f"last_update={o['last_update']}",
        f"delay_reason={o['delay_reason'] or '—'}",
    ])

def _return_context(sku: str) -> str:
    products = _load_json(DATA / "products.json")
    p = next((x for x in products if x["sku"] == sku), None)
    if not p:
        return f"[PRODUCT]\nNo existe el SKU {sku}."
    return "\n".join([
        "[PRODUCT]",
        f"sku={p['sku']}",
        f"name={p['name']}",
        f"category={p['category']}",
        f"returnable={'sí' if p['returnable'] else 'no'}",
        "\n[POLICY]",
        _load_policy()
    ])

def _render(template: str, context: str, **vars) -> tuple[str, str]:
    t = template.replace("{{context}}", context)
    for k, v in vars.items():
        t = t.replace(f"{{{{{k}}}}}", str(v))
    sys, usr = "", t
    if "SYSTEM:" in t and "USER:" in t:
        sys = t.split("USER:", 1)[0].replace("SYSTEM:", "").strip()
        usr = t.split("USER:", 1)[1].strip()
    return sys, usr

def _chat(system_msg: str, user_msg: str) -> str:
    r = client.chat.completions.create(
        model=SETTINGS["general"]["model"],
        temperature=SETTINGS["general"]["temperature"],
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )
    return r.choices[0].message.content.strip()

def _format_docs(docs):
    # Si tu RAGRetriever ya trae .format_context(docs), puedes usarlo.
    # Este helper es genérico por si no lo tienes:
    out = []
    for d in docs:
        src = d.metadata.get("source", "source")
        out.append(f"[{src}] {d.page_content.strip()}")
    return "\n\n".join(out)

def _order_rag_context(trk: str) -> str:
    """
    Pide a RAG fragmentos relevantes para 'estado de pedido' y políticas de envío/retraso.
    """
    q = (
        f"Consulta de estado para el pedido con tracking {trk}. "
        f"¿Qué dicen las políticas de envío, demoras y rastreo? "
        f"Devolver fragmentos útiles para explicar al cliente."
    )
    docs = rag.get_relevant_chunks(q)
    return _format_docs(docs) if docs else ""

def _return_rag_context(sku: str, days: int, opened: bool) -> str:
    """
    Pide a RAG fragmentos de política de devoluciones + ficha del producto.
    """
    q = (
        f"Solicitud de devolución para SKU {sku}. "
        f"Días desde la entrega: {days}. Abierto: {opened}. "
        f"Devolver política aplicable (restricciones por categoría, plazos) y detalles del producto."
    )
    docs = rag.get_relevant_chunks(q)
    return _format_docs(docs) if docs else ""

def main():
    ap = argparse.ArgumentParser(description="EcoMarket – Taller Fase 3 (simple)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    o = sub.add_parser("order", help="Consultar estado de pedido")
    o.add_argument("--tracking", required=True)

    r = sub.add_parser("return", help="Guía de devolución")
    r.add_argument("--sku", required=True)
    r.add_argument("--days_since_delivery", type=int, required=True)
    r.add_argument("--opened", action="store_true")

    f = sub.add_parser("faq", help="Preguntas frecuentes (usa solo RAG)")
    f.add_argument("--question", required=True, help="Pregunta en lenguaje natural")

    args = ap.parse_args()
    prompts = SETTINGS["prompts"]

    if args.cmd == "order":
        # Usar únicamente el índice RAG como contexto (no consultas locales a orders.json)
        rag_ctx = _order_rag_context(args.tracking)
        if not rag_ctx:
            rag_ctx = "[RAG]\nNo se han encontrado fragmentos relevantes en el índice."
        ctx = f"[RAG]\n{rag_ctx}"
        sys, usr = _render(prompts["order_status"], ctx, tracking=args.tracking)
        print(_chat(sys, f"{usr}\n\n{ctx}"))
    elif args.cmd == "return":
        # Usar únicamente el índice RAG como contexto para devoluciones
        rag_ctx = _return_rag_context(args.sku, args.days_since_delivery, args.opened)
        if not rag_ctx:
            rag_ctx = "[RAG]\nNo se han encontrado fragmentos relevantes en el índice."
        ctx = f"[RAG]\n{rag_ctx}"
        name = ""  # No consultamos products.json localmente cuando usamos solo RAG
        sys, usr = _render(
            prompts["return_policy"], ctx,
            sku=args.sku,
            days_since_delivery=args.days_since_delivery,
            opened=str(args.opened).lower(),
            name=name
        )
        usr = (
            f"{usr}\n\n[INPUTS]\n"
            f"sku={args.sku}\n"
            f"days_since_delivery={args.days_since_delivery}\n"
            f"abierto={'true' if args.opened else 'false'}\n\n{ctx}"
        )
        print(_chat(sys, usr))
    elif args.cmd == "faq":
        # FAQ handler: pregunta libre que usa únicamente el índice RAG
        q = args.question
        # Reusar retriever para buscar fragmentos relevantes a la pregunta
        docs = rag.get_relevant_chunks(q)
        rag_ctx = _format_docs(docs) if docs else "[RAG]\nNo se han encontrado fragmentos relevantes en el índice."
        ctx = f"[RAG]\n{rag_ctx}"
        # Usar un prompt genérico 'faq' si existe, sino usar el system/user por defecto
        if "faq" in prompts:
            sys, usr = _render(prompts["faq"], ctx, question=q)
        else:
            sys, usr = "", q
        print(_chat(sys, f"{usr}\n\n{ctx}"))

if __name__ == "__main__":
    main()
