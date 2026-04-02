import Image from "next/image"

type HeaderProps = {
  onOpenOnboarding?: () => void
}

export default function Header({ onOpenOnboarding }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 z-50 w-full border-b border-white/10 bg-black/40 backdrop-blur-md">
      <div
        className="mx-auto flex min-h-16 flex-col gap-3 px-4 py-3 sm:px-6 md:flex-row md:items-center md:justify-between md:py-0"
        style={{ maxWidth: "1200px" }}
      >
        <div className="flex items-center gap-3">
          <Image
            src="/lava lamp logo.png"
            alt="EntropyLab logo"
            width={40}
            height={40}
            className="h-10 w-10 object-contain"
          />
          <div className="text-xl font-bold tracking-tight text-white">
            Entropy<span className="text-red-600">Lab</span>
          </div>
        </div>

        <nav className="flex flex-wrap items-center gap-4 sm:gap-6 md:justify-end">
          <a href="#" className="text-sm font-medium text-white transition-colors hover:text-teal-300">
            Como funciona
          </a>
          <a href="#" className="text-sm font-medium text-white transition-colors hover:text-teal-300">
            Documentaci&oacute;n
          </a>
          <a
            href="https://github.com/Lord-Pat/EntropyLab"
            target="_blank"
            rel="noreferrer"
            className="text-sm font-medium text-white transition-colors hover:text-teal-300"
          >
            Github
          </a>
          <button
            type="button"
            onClick={onOpenOnboarding}
            className="rounded-full bg-red-600 px-5 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-700"
          >
            Obtener claves
          </button>
        </nav>
      </div>
    </header>
  )
}
