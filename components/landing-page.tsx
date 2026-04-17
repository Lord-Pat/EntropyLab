"use client"

import { useEffect, useRef, useState } from "react"

import VideoBackground from "@/components/background/video-background"
import Footer from "@/components/footer"
import Header from "@/components/header"
import OnboardingModal from "@/components/onboarding-modal"
import { Button } from "@/components/ui/button"

function useInView(threshold = 0.25) {
  const ref = useRef<HTMLDivElement>(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setVisible(true)
      },
      { threshold }
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [threshold])

  return { ref, visible }
}

export default function LandingPage() {
  const [isOnboardingOpen, setIsOnboardingOpen] = useState(false)
  const scrollRef = useRef<HTMLElement>(null)
  const s1 = useInView(0.1)
  const s2 = useInView()
  const s3 = useInView()

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = 0
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

      <main
        ref={scrollRef}
        className="h-screen snap-y snap-mandatory overflow-y-scroll"
        style={{ scrollbarWidth: "none" }}
      >
        {/* Section 1 — Hero */}
        <section className="relative flex h-screen snap-start items-center overflow-hidden">
          <VideoBackground />
          <div
            ref={s1.ref}
            className={`mx-auto w-full px-6 transition-all duration-700 ease-out ${
              s1.visible ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
            }`}
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
        <section className="flex h-auto snap-start items-center border-y border-white/10 bg-black py-12.5">
          <div
            ref={s2.ref}
            className={`mx-auto w-full px-6 transition-all duration-700 ease-out ${
              s2.visible ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
            }`}
            style={{ maxWidth: "1200px" }}
          >
            <div className="grid grid-cols-1 gap-12 md:grid-cols-3 md:gap-16">
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>L&aacute;mpara en tiempo real</h3>
                <hr style={{ borderColor: "#fafafa", borderWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  Este es el feed directo de la c&aacute;mara apuntando a nuestra l&aacute;mpara de
                  lava. Cada p&iacute;xel, cada movimiento, contribuye a la generaci&oacute;n de tu
                  clave.
                </p>
                <Button asChild className="mt-6 w-fit rounded-full text-xs uppercase hover:opacity-80" style={{ backgroundColor: "#fafafa", color: "#0a0a0a" }}>
                  <a href="#">Saber más</a>
                </Button>
              </div>
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>
                  Tus claves, generadas por <span className="text-red-500">lava</span>
                </h3>
                <hr style={{ borderColor: "#fafafa", borderTopWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                </p>
                <Button asChild className="mt-6 w-fit rounded-full text-xs uppercase hover:opacity-80" style={{ backgroundColor: "#fafafa", color: "#0a0a0a" }}>
                  <a href="#">Saber más</a>
                </Button>
              </div>
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>Construido en abierto, para todos</h3>
                <hr style={{ borderColor: "#fafafa", borderTopWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  EntropyLab naci&oacute; con la convicci&oacute;n de que la seguridad real no puede
                  depender de cajas negras. Por eso todo lo que construimos es p&uacute;blico:
                  puedes revisar c&oacute;mo capturamos la entrop&iacute;a, c&oacute;mo generamos las claves
                  y c&oacute;mo te las entregamos.
                </p>
                <Button asChild className="mt-6 w-fit rounded-full text-xs uppercase hover:opacity-80" style={{ backgroundColor: "#fafafa", color: "#0a0a0a" }}>
                  <a href="#">Saber más</a>
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Section 3 — Three pillars (duplicate) */}
        <section className="flex h-auto snap-start items-center border-y border-white/10 bg-black py-12.5">
          <div
            ref={s3.ref}
            className={`mx-auto w-full px-6 transition-all duration-700 ease-out ${
              s3.visible ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
            }`}
            style={{ maxWidth: "1200px" }}
          >
            <div className="grid grid-cols-1 gap-12 md:grid-cols-3 md:gap-16">
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>L&aacute;mpara en tiempo real</h3>
                <hr style={{ borderColor: "#fafafa", borderWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  Este es el feed directo de la c&aacute;mara apuntando a nuestra l&aacute;mpara de
                  lava. Cada p&iacute;xel, cada movimiento, contribuye a la generaci&oacute;n de tu
                  clave.
                </p>
                <Button asChild className="mt-6 w-fit rounded-full text-xs uppercase hover:opacity-80" style={{ backgroundColor: "#fafafa", color: "#0a0a0a" }}>
                  <a href="#">Saber más</a>
                </Button>
              </div>
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>
                  Tus claves, generadas por <span className="text-red-500">lava</span>
                </h3>
                <hr style={{ borderColor: "#fafafa", borderTopWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                </p>
                <Button asChild className="mt-6 w-fit rounded-full text-xs uppercase hover:opacity-80" style={{ backgroundColor: "#fafafa", color: "#0a0a0a" }}>
                  <a href="#">Saber más</a>
                </Button>
              </div>
              <div className="flex flex-col text-left">
                <h3 className="font-bold text-white" style={{ fontSize: "2em", lineHeight: "1em", letterSpacing: "-0.03em" }}>Construido en abierto, para todos</h3>
                <hr style={{ borderColor: "#fafafa", borderTopWidth: "0.5px", marginTop: "25px", marginBottom: "25px" }} />
                <p className="text-base text-gray-300" style={{ fontWeight: 200, letterSpacing: "-0.03em", lineHeight: "1.3em" }}>
                  EntropyLab naci&oacute; con la convicci&oacute;n de que la seguridad real no puede
                  depender de cajas negras. Por eso todo lo que construimos es p&uacute;blico:
                  puedes revisar c&oacute;mo capturamos la entrop&iacute;a, c&oacute;mo generamos las claves
                  y c&oacute;mo te las entregamos.
                </p>
                <Button asChild className="mt-6 w-fit rounded-full text-xs uppercase hover:opacity-80" style={{ backgroundColor: "#fafafa", color: "#0a0a0a" }}>
                  <a href="#">Saber más</a>
                </Button>
              </div>
            </div>
          </div>
        </section>

      </main>

      <Footer />

      <OnboardingModal
        isOpen={isOnboardingOpen}
        onClose={() => setIsOnboardingOpen(false)}
      />
    </>
  )
}
