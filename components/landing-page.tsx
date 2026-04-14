"use client"

import { useEffect, useState } from "react"

import VideoBackground from "@/components/background/video-background"
import Footer from "@/components/footer"
import Header from "@/components/header"
import OnboardingModal from "@/components/onboarding-modal"

export default function LandingPage() {
  const [isOnboardingOpen, setIsOnboardingOpen] = useState(false)

  useEffect(() => {
    if (!isOnboardingOpen) {
      return
    }

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsOnboardingOpen(false)
      }
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
      <VideoBackground />
      <main>
        <Header onOpenOnboarding={openOnboarding} />

        <section className="min-h-screen pt-28 md:pt-16">
          <div
            className="mx-auto flex min-h-[calc(100vh-4rem)] items-center px-6"
            style={{ maxWidth: "1200px" }}
          >
            <div className="max-w-2xl lg:max-w-[50%]">
              <h1 className="text-left text-4xl font-black leading-[1em] tracking-tight text-white sm:text-5xl md:text-6xl">
                Claves generadas a trav&eacute;s de la aleatoriedad de la lava
              </h1>
              <p className="mt-6 text-lg leading-[1em] text-gray-300">
                EntropyLab captura el movimiento impredecible de l&aacute;mparas de lava para
                generar claves criptogr&aacute;ficas de alta entrop&iacute;a. Sin algoritmos, sin
                patrones: entrop&iacute;a f&iacute;sica pura. 100% open source.
              </p>
            </div>
          </div>
        </section>

        <section className="border-y border-white/10 bg-black py-16">
          <div className="mx-auto px-6" style={{ maxWidth: "1200px" }}>
            <div className="flex items-center gap-12">
              <div className="flex-1 text-left">
                <h2 className="mb-4 text-3xl font-bold text-white">L&aacute;mpara en tiempo real</h2>
                <p className="text-base text-gray-300">
                  Este es el feed directo de la c&aacute;mara apuntando a nuestra l&aacute;mpara de
                  lava. Cada p&iacute;xel, cada movimiento, contribuye a la generaci&oacute;n de tu
                  clave.
                </p>
              </div>
              <div className="flex-1">
                <div className="aspect-4/3 w-full overflow-hidden rounded-lg bg-teal-300">
                  <video
                    autoPlay
                    loop
                    muted
                    playsInline
                    aria-label="Movimiento de una lampara de lava"
                    className="h-full w-full object-cover"
                  >
                    <source src="/Lava_lamp_video_movement.mp4" type="video/mp4" />
                  </video>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="py-24">
          <div
            className="mx-auto flex flex-col items-center justify-center gap-6 px-6"
            style={{ maxWidth: "1200px" }}
          >
            <h1 className="text-center text-4xl font-black tracking-tight text-white sm:text-5xl md:text-6xl">
              Tus claves, generadas por <span className="text-red-500">lava</span>
            </h1>
            <p className="max-w-2xl text-center text-lg leading-8 text-gray-300 md:text-xl">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </p>
            <button
              type="button"
              onClick={openOnboarding}
              className="rounded-full bg-red-600 px-8 py-3 text-base font-semibold text-white transition-colors hover:bg-red-700"
            >
              Obtener claves
            </button>
          </div>
        </section>

        <section className="border-y border-white/10 bg-black/50 py-16 backdrop-blur-md">
          <div className="mx-auto px-6" style={{ maxWidth: "1200px" }}>
            <div className="flex flex-col gap-10 md:flex-row md:items-center md:gap-12">
              <div className="flex flex-1 justify-center md:justify-start">
                <a
                  href="https://github.com/Lord-Pat/EntropyLab"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-3 rounded-full border border-white/20 bg-white/5 px-6 py-3 text-base font-semibold text-white transition-colors hover:border-white/40 hover:bg-white/10 md:ml-16"
                >
                  <svg
                    aria-hidden="true"
                    viewBox="0 0 24 24"
                    className="h-5 w-5 fill-current"
                  >
                    <path d="M12 .5C5.65.5.5 5.66.5 12.03c0 5.1 3.29 9.42 7.86 10.95.57.11.78-.25.78-.55 0-.27-.01-1.17-.02-2.12-3.2.7-3.88-1.36-3.88-1.36-.52-1.34-1.28-1.69-1.28-1.69-1.05-.72.08-.71.08-.71 1.16.08 1.77 1.2 1.77 1.2 1.03 1.77 2.7 1.26 3.35.96.1-.75.4-1.26.73-1.55-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.3 1.19-3.11-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.19 1.19a10.9 10.9 0 0 1 5.8 0c2.21-1.5 3.18-1.19 3.18-1.19.64 1.59.24 2.77.12 3.06.74.81 1.19 1.85 1.19 3.11 0 4.43-2.68 5.4-5.24 5.69.41.35.78 1.05.78 2.12 0 1.53-.01 2.76-.01 3.14 0 .31.2.67.79.55a11.53 11.53 0 0 0 7.85-10.95C23.5 5.66 18.35.5 12 .5Z" />
                  </svg>
                  Ver en GitHub
                </a>
              </div>
              <div className="flex-1 text-left">
                <h2 className="mb-4 text-3xl font-bold text-white">Construido en abierto, para todos</h2>
                <p className="text-base text-gray-300">
                  EntropyLab naci&oacute; con la convicci&oacute;n de que la seguridad real no puede
                  depender de cajas negras. Por eso todo lo que construimos es p&uacute;blico:
                  puedes revisar c&oacute;mo capturamos la entrop&iacute;a, c&oacute;mo generamos las claves
                  y c&oacute;mo te las entregamos. Sin sorpresas, sin letra peque&ntilde;a.
                </p>
              </div>
            </div>
          </div>
        </section>

        <Footer />
      </main>

      <OnboardingModal
        isOpen={isOnboardingOpen}
        onClose={() => setIsOnboardingOpen(false)}
      />
    </>
  )
}
