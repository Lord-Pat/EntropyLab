import { NextResponse } from "next/server"

const ONBOARDING_API_URL = process.env.ONBOARDING_API_URL

export async function POST(request: Request) {
  if (!ONBOARDING_API_URL) {
    return NextResponse.json(
      { error: "Falta configurar la variable ONBOARDING_API_URL." },
      { status: 500 }
    )
  }

  let payload: unknown

  try {
    payload = await request.json()
  } catch {
    return NextResponse.json({ error: "El cuerpo de la solicitud no es valido." }, { status: 400 })
  }

  try {
    const upstreamResponse = await fetch(ONBOARDING_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      cache: "no-store",
    })

    const contentType = upstreamResponse.headers.get("content-type")
    const contentDisposition = upstreamResponse.headers.get("content-disposition")

    if (!upstreamResponse.ok) {
      const errorText = await upstreamResponse.text()

      try {
        const errorPayload = JSON.parse(errorText) as { error?: string; message?: string }
        return NextResponse.json(
          { error: errorPayload.error ?? errorPayload.message ?? "La API devolvio un error." },
          { status: upstreamResponse.status }
        )
      } catch {
        return NextResponse.json(
          { error: errorText || "La API devolvio un error." },
          { status: upstreamResponse.status }
        )
      }
    }

    if (contentType?.includes("application/json")) {
      const data = await upstreamResponse.json()
      return NextResponse.json(data, { status: upstreamResponse.status })
    }

    const blob = await upstreamResponse.blob()
    const headers = new Headers()

    if (contentType) {
      headers.set("Content-Type", contentType)
    }

    if (contentDisposition) {
      headers.set("Content-Disposition", contentDisposition)
    }

    return new Response(blob, {
      status: upstreamResponse.status,
      headers,
    })
  } catch {
    return NextResponse.json(
      { error: "No se pudo conectar con la API de onboarding." },
      { status: 502 }
    )
  }
}
