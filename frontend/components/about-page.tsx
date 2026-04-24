import VideoBackground from "@/components/background/video-background"
import Footer from "@/components/footer"
import Header from "@/components/header"

const members = [
  {
    name: "Aarón Martínez",
    text: "Espacio para una descripcion breve de hasta 100 caracteres.",
    linkedin: "https://www.linkedin.com/in/aaron-martinez-nieto-9183a1b2/",
    github: "https://github.com/AaronMartinez91",
    accent: "#ef4444",
  },
  {
    name: "Patrick Carbajal",
    text: "Espacio para una descripcion breve de hasta 100 caracteres.",
    linkedin: "https://www.linkedin.com/in/patrick-carbajal-malato-0a27342a4/",
    github: "https://github.com/Lord-Pat",
    accent: "#5eead4",
  },
]

function MemberImage({ accent }: { accent: string }) {
  return (
    <svg
      viewBox="0 0 320 320"
      role="img"
      aria-label="Imagen del integrante"
      className="h-full w-full"
    >
      <rect width="320" height="320" fill="#111111" />
      <circle cx="160" cy="126" r="58" fill={accent} opacity="0.9" />
      <path
        d="M74 292c12-62 48-94 86-94s74 32 86 94"
        fill={accent}
        opacity="0.75"
      />
      <circle cx="138" cy="120" r="8" fill="#0a0a0a" />
      <circle cx="182" cy="120" r="8" fill="#0a0a0a" />
      <path
        d="M136 152c16 14 34 14 50 0"
        fill="none"
        stroke="#0a0a0a"
        strokeLinecap="round"
        strokeWidth="8"
      />
      <path
        d="M24 42c42-26 92-34 150-24 48 8 88 30 122 66"
        fill="none"
        stroke="#ffffff"
        strokeLinecap="round"
        strokeWidth="4"
        opacity="0.18"
      />
    </svg>
  )
}

function GithubIcon() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      className="h-5 w-5 fill-current"
    >
      <path d="M12 .5C5.65.5.5 5.66.5 12.03c0 5.1 3.29 9.42 7.86 10.95.57.11.78-.25.78-.55 0-.27-.01-1.17-.02-2.12-3.2.7-3.88-1.36-3.88-1.36-.52-1.34-1.28-1.69-1.28-1.69-1.05-.72.08-.71.08-.71 1.16.08 1.77 1.2 1.77 1.2 1.03 1.77 2.7 1.26 3.35.96.1-.75.4-1.26.73-1.55-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.3 1.19-3.11-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.19 1.19a10.9 10.9 0 0 1 5.8 0c2.21-1.5 3.18-1.19 3.18-1.19.64 1.59.24 2.77.12 3.06.74.81 1.19 1.85 1.19 3.11 0 4.43-2.68 5.4-5.24 5.69.41.35.78 1.05.78 2.12 0 1.53-.01 2.76-.01 3.14 0 .31.2.67.79.55a11.53 11.53 0 0 0 7.85-10.95C23.5 5.66 18.35.5 12 .5Z" />
    </svg>
  )
}

function LinkedinIcon() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      className="h-5 w-5 fill-current"
    >
      <path d="M20.45 20.45h-3.56v-5.58c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.44-2.13 2.94v5.68H9.35V8.98h3.42v1.57h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.29ZM5.33 7.41a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12Zm1.78 13.04H3.55V8.98h3.56v11.47ZM22.22 0H1.77C.8 0 0 .78 0 1.75v20.5C0 23.22.8 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.75V1.75C24 .78 23.2 0 22.22 0Z" />
    </svg>
  )
}

export default function AboutPage() {
  return (
    <>
      <VideoBackground />
      <main>
        <Header />

        <section className="min-h-screen pt-28 md:pt-16">
          <div
            className="mx-auto flex min-h-[calc(100vh-4rem)] flex-col justify-center px-6 py-16"
            style={{ maxWidth: "1200px" }}
          >
            <div className="mb-12 max-w-2xl">
              <p className="mb-4 text-sm font-semibold tracking-[0.2em] text-teal-200 uppercase">
                Sobre nosotros
              </p>
              <h1 className="text-4xl leading-[1em] font-black tracking-tight text-white sm:text-5xl md:text-6xl">
                El equipo
              </h1>
            </div>

            <div className="grid gap-8 md:grid-cols-2">
              {members.map((member) => (
                <article
                  key={member.name}
                  className="border border-white/10 bg-black/50 p-5 text-white backdrop-blur-md"
                >
                  <div className="aspect-square w-full overflow-hidden rounded-lg border border-white/10 bg-black">
                    <MemberImage accent={member.accent} />
                  </div>

                  <div className="pt-6">
                    <h2 className="text-2xl font-bold">{member.name}</h2>
                    <p className="mt-3 min-h-12 max-w-md text-base leading-6 text-gray-300">
                      {member.text}
                    </p>

                    <div className="mt-6 flex gap-3">
                      <a
                        href={member.linkedin}
                        aria-label={`LinkedIn de ${member.name}`}
                        className="inline-flex h-11 w-11 items-center justify-center rounded-lg border border-white/20 bg-white/5 text-white transition-colors hover:border-teal-200 hover:text-teal-200"
                      >
                        <LinkedinIcon />
                      </a>
                      <a
                        href={member.github}
                        aria-label={`GitHub de ${member.name}`}
                        className="inline-flex h-11 w-11 items-center justify-center rounded-lg border border-white/20 bg-white/5 text-white transition-colors hover:border-teal-200 hover:text-teal-200"
                      >
                        <GithubIcon />
                      </a>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <Footer />
      </main>
    </>
  )
}
