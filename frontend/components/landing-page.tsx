"use client"

import { useEffect, useRef, useState } from "react"

import VideoBackground from "@/components/background/video-background"
import Footer from "@/components/footer"
import Header from "@/components/header"
import OnboardingModal from "@/components/onboarding-modal"

function useCountUp(target: number) {
  const [count, setCount] = useState(0)
  const [ref, setRef] = useState<HTMLDivElement | null>(null)
  const currentCount = useRef(0)
  const hasStarted = useRef(false)

  const animateTo = (from: number, to: number, duration: number) => {
    const startTime = performance.now()
    const tick = (now: number) => {
      const progress = Math.min((now - startTime) / duration, 1)
      const value = Math.floor(from + progress * (to - from))
      currentCount.current = value
      setCount(value)
      if (progress < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  }

  useEffect(() => {
    if (!ref) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting || hasStarted.current) return
        observer.disconnect()
        hasStarted.current = true
        animateTo(0, target, 1500)
      },
      { threshold: 0.5 }
    )
    observer.observe(ref)
    return () => observer.disconnect()
  }, [ref, target])

  useEffect(() => {
    if (!hasStarted.current) return
    animateTo(currentCount.current, target, 1500)
  }, [target])

  return { count, setRef }
}

export default function LandingPage() {
  const [isOnboardingOpen, setIsOnboardingOpen] = useState(false)
  const [totalKeys, setTotalKeys] = useState(0)
  const { count, setRef: setCounterRef } = useCountUp(totalKeys)

  const handleKeysGenerated = (quantity: number) => {
    setTotalKeys((prev) => prev + quantity)
  }

  useEffect(() => {
    if ("scrollRestoration" in history) history.scrollRestoration = "manual"
    window.scrollTo(0, 0)
  }, [])

  useEffect(() => {
    let active = true
    const controller = new AbortController()

    async function connectSSE() {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/keys/count/stream`, {
          headers: { "ngrok-skip-browser-warning": "true" },
          signal: controller.signal,
        })
        if (!res.body) return
        const reader = res.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ""
        while (active) {
          const { done, value } = await reader.read()
          if (done) break
          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split("\n")
          buffer = lines.pop() ?? ""
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const total = parseInt(line.slice(6), 10)
              if (!isNaN(total)) setTotalKeys(total)
            }
          }
        }
      } catch {
        // conexión cerrada o abortada
      }
    }

    connectSSE()
    return () => {
      active = false
      controller.abort()
    }
  }, [])

  useEffect(() => {
    if (!isOnboardingOpen) return
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsOnboardingOpen(false)
    }
    document.body.style.overflow = "hidden"
    window.addEventListener("keydown", handleEscape)
    return () => {
      document.body.style.overflow = ""
      window.removeEventListener("keydown", handleEscape)
    }
  }, [isOnboardingOpen])

  const openOnboarding = () => setIsOnboardingOpen(true)

  return (
    <>
      <Header onOpenOnboarding={openOnboarding} />

      <main className="min-h-screen">
        {/* Section 1 — Hero */}
        <section className="relative flex min-h-screen items-center overflow-hidden">
          <VideoBackground />
          <div
            className="mx-auto w-full px-6"
            style={{ maxWidth: "1200px" }}
          >
            <div className="max-w-2xl lg:max-w-[100%]">
              <h1 className="text-center font-black leading-[1em] text-white" style={{ fontSize: "6em", letterSpacing: "-0.04em", textShadow: "0px 0px 7px rgba(10,10,10,0.97)" }}>
                Claves generadas a través de la aleatoriedad de la lava
              </h1>
              <p className="mt-6 text-gray-300" style={{ textAlign: "center", fontSize: "1.5em", fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1em", textShadow: "0px 0px 7px rgba(10,10,10,0.97)" }}>
                EntropyLab captura el movimiento impredecible de l&aacute;mparas de lava para
                generar <span style={{ fontWeight: 700 }}>claves criptogr&aacute;ficas de alta entrop&iacute;a</span>. Sin algoritmos, sin
                patrones: entrop&iacute;a f&iacute;sica pura. 100% open source.
              </p>
            </div>
          </div>
        </section>

        {/* Section 2 — Three pillars */}
        <section className="flex h-auto items-center border-y border-white/10 py-12.5" style={{ backgroundColor: "#111111" }}>
          <div
            className="mx-auto w-full px-6"
            style={{ maxWidth: "1200px" }}
          >
            <div className="grid grid-cols-1 gap-12 md:grid-cols-3 md:gap-16">
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>Entropía física, no algoritmos</h3>
                <hr style={{ borderColor: "#fafafa", borderWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  El movimiento caótico de la lava dentro de una lámpara es imposible de predecir o replicar. 
                  EntropyLab captura ese caos frame a frame con una cámara, extrae las diferencias entre imágenes consecutivas y las convierte en bits de entropía real.
                  Sin semillas artificiales, sin generadores pseudoaleatorios: la fuente es el mundo físico.
                </p>
              </div>
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>
                  Validadas con estándares científicos
                </h3>
                <hr style={{ borderColor: "#fafafa", borderTopWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  Cada versión del algoritmo se somete a los tests estadísticos NIST SP800-22, el estándar de referencia en criptografía para validar generadores aleatorios.
                  Medimos también la entropía de Shannon de cada muestra. Los resultados son públicos y comparables entre versiones.
                  Puedes verificar tú mismo que las claves superan los umbrales de aleatoriedad.
                </p>
              </div>
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>Construido en abierto, para todos</h3>
                <hr style={{ borderColor: "#fafafa", borderTopWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  EntropyLab nació con la convicción de que la seguridad real no puede depender de cajas negras. Por eso todo lo que construimos es público:
                  puedes revisar cómo capturamos la entropía, cómo generamos las claves y cómo te las entregamos. El código fuente está disponible en GitHub 
                  para que cualquiera pueda auditarlo, replicarlo o construir sobre él.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Contenido Counter visual para clientes */}
        <section className="flex h-auto items-center border-y border-white/10 py-12.5" style={{ backgroundColor: "#111111" }}>
          <div
            className="mx-auto w-full px-6"
            style={{ maxWidth: "1200px" }}
          > 
            <div ref={setCounterRef}>
              <h3 className="font-bold text-white text-center" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>Claves generadas</h3>
              <p className="text-center text-red-400 text-5xl font-bold mt-4">{count.toLocaleString()}</p>
            </div>
          </div>
        </section>

        {/* Section 3 — Sobre nosotros */}
        <section id="sobre-nosotros" className="flex h-auto items-center border-y border-white/10 py-16" style={{ backgroundColor: "#1a1a1a" }}>
          <div
            className="mx-auto w-full px-6"
            style={{ maxWidth: "1200px" }}
          >
            <div className="grid grid-cols-1 items-center gap-12 md:grid-cols-2 md:gap-16">
              {/* Left: shared team photo */}
              <div className="aspect-4/3 w-full overflow-hidden rounded-2xl border border-white/10 bg-white/5">
                {/* Replace src with your actual team photo, e.g. /team-photo.jpg */}
                <div className="flex h-full items-center justify-center text-sm text-gray-600">
                  Foto conjunta del equipo
                </div>
              </div>

              {/* Right: team members */}
              <div className="flex flex-col">
                <p className="mb-6 text-xs font-semibold uppercase tracking-[0.2em] text-red-400">
                  Sobre nosotros
                </p>

                {/* Aarón */}
                <div className="flex flex-col">
                  <h3 className="font-bold text-white" style={{ fontSize: "1.5em", letterSpacing: "-0.03em" }}>
                    Aarón Martínez
                  </h3>
                  <p className="mt-2 text-gray-400" style={{ fontWeight: 200, letterSpacing: "-0.02em", lineHeight: "1.5em", fontSize: "0.95em" }}>
                    Aquí irá tu descripción personal: rol, motivación o dato curioso. Unas veinte palabras funcionan bien.
                  </p>
                  <div className="mt-4 flex gap-3">
                    <a
                      href="https://www.linkedin.com/in/aaron-martinez-nieto-9183a1b2/"
                      target="_blank"
                      rel="noreferrer"
                      aria-label="LinkedIn de Aarón"
                      className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/20 bg-white/5 text-white transition-colors outline-none hover:border-red-500/60 hover:text-red-400"
                    >
                      <svg aria-hidden="true" viewBox="0 0 24 24" className="h-4 w-4 fill-current">
                        <path d="M20.45 20.45h-3.56v-5.58c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.44-2.13 2.94v5.68H9.35V8.98h3.42v1.57h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.29ZM5.33 7.41a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12Zm1.78 13.04H3.55V8.98h3.56v11.47ZM22.22 0H1.77C.8 0 0 .78 0 1.75v20.5C0 23.22.8 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.75V1.75C24 .78 23.2 0 22.22 0Z" />
                      </svg>
                    </a>
                    <a
                      href="https://github.com/AaronMartinez91"
                      target="_blank"
                      rel="noreferrer"
                      aria-label="GitHub de Aarón"
                      className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/20 bg-white/5 text-white transition-colors outline-none hover:border-red-500/60 hover:text-red-400"
                    >
                      <svg aria-hidden="true" viewBox="0 0 24 24" className="h-4 w-4 fill-current">
                        <path d="M12 .5C5.65.5.5 5.66.5 12.03c0 5.1 3.29 9.42 7.86 10.95.57.11.78-.25.78-.55 0-.27-.01-1.17-.02-2.12-3.2.7-3.88-1.36-3.88-1.36-.52-1.34-1.28-1.69-1.28-1.69-1.05-.72.08-.71.08-.71 1.16.08 1.77 1.2 1.77 1.2 1.03 1.77 2.7 1.26 3.35.96.1-.75.4-1.26.73-1.55-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.3 1.19-3.11-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.19 1.19a10.9 10.9 0 0 1 5.8 0c2.21-1.5 3.18-1.19 3.18-1.19.64 1.59.24 2.77.12 3.06.74.81 1.19 1.85 1.19 3.11 0 4.43-2.68 5.4-5.24 5.69.41.35.78 1.05.78 2.12 0 1.53-.01 2.76-.01 3.14 0 .31.2.67.79.55a11.53 11.53 0 0 0 7.85-10.95C23.5 5.66 18.35.5 12 .5Z" />
                      </svg>
                    </a>
                  </div>
                </div>

                <hr style={{ borderColor: "rgba(255,255,255,0.1)", margin: "28px 0" }} />

                {/* Patrick */}
                <div className="flex flex-col">
                  <h3 className="font-bold text-white" style={{ fontSize: "1.5em", letterSpacing: "-0.03em" }}>
                    Patrick Carbajal
                  </h3>
                  <p className="mt-2 text-gray-400" style={{ fontWeight: 200, letterSpacing: "-0.02em", lineHeight: "1.5em", fontSize: "0.95em" }}>
                    Aquí irá tu descripción personal: rol, motivación o dato curioso. Unas veinte palabras funcionan bien.
                  </p>
                  <div className="mt-4 flex gap-3">
                    <a
                      href="https://www.linkedin.com/in/patrick-carbajal-malato-0a27342a4/"
                      target="_blank"
                      rel="noreferrer"
                      aria-label="LinkedIn de Patrick"
                      className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/20 bg-white/5 text-white transition-colors outline-none hover:border-red-500/60 hover:text-red-400"
                    >
                      <svg aria-hidden="true" viewBox="0 0 24 24" className="h-4 w-4 fill-current">
                        <path d="M20.45 20.45h-3.56v-5.58c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.44-2.13 2.94v5.68H9.35V8.98h3.42v1.57h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.29ZM5.33 7.41a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12Zm1.78 13.04H3.55V8.98h3.56v11.47ZM22.22 0H1.77C.8 0 0 .78 0 1.75v20.5C0 23.22.8 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.75V1.75C24 .78 23.2 0 22.22 0Z" />
                      </svg>
                    </a>
                    <a
                      href="https://github.com/Lord-Pat"
                      target="_blank"
                      rel="noreferrer"
                      aria-label="GitHub de Patrick"
                      className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/20 bg-white/5 text-white transition-colors outline-none hover:border-red-500/60 hover:text-red-400"
                    >
                      <svg aria-hidden="true" viewBox="0 0 24 24" className="h-4 w-4 fill-current">
                        <path d="M12 .5C5.65.5.5 5.66.5 12.03c0 5.1 3.29 9.42 7.86 10.95.57.11.78-.25.78-.55 0-.27-.01-1.17-.02-2.12-3.2.7-3.88-1.36-3.88-1.36-.52-1.34-1.28-1.69-1.28-1.69-1.05-.72.08-.71.08-.71 1.16.08 1.77 1.2 1.77 1.2 1.03 1.77 2.7 1.26 3.35.96.1-.75.4-1.26.73-1.55-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.3 1.19-3.11-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.19 1.19a10.9 10.9 0 0 1 5.8 0c2.21-1.5 3.18-1.19 3.18-1.19.64 1.59.24 2.77.12 3.06.74.81 1.19 1.85 1.19 3.11 0 4.43-2.68 5.4-5.24 5.69.41.35.78 1.05.78 2.12 0 1.53-.01 2.76-.01 3.14 0 .31.2.67.79.55a11.53 11.53 0 0 0 7.85-10.95C23.5 5.66 18.35.5 12 .5Z" />
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

      </main>

      <Footer />

      <OnboardingModal
        isOpen={isOnboardingOpen}
        onClose={() => setIsOnboardingOpen(false)}
        onSuccess={handleKeysGenerated}
      />
    </>
  )
}
