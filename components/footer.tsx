import Image from "next/image"
import Link from "next/link"

export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-black/50 py-12 backdrop-blur-md">
      <div
        className="mx-auto flex flex-col items-start gap-8 px-4 sm:px-6 md:flex-row md:items-center md:justify-between"
        style={{ maxWidth: "1200px" }}
      >
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/lava lamp logo.png"
            alt="EntropyLab logo"
            width={40}
            height={40}
            className="h-10 w-10 object-contain invert"
          />
          <div className="text-xl font-bold tracking-tight text-white">
            Entropy<span className="text-red-600">Lab</span>
          </div>
        </Link>

        <nav className="flex flex-wrap gap-4 sm:gap-8 md:justify-end">
          <Link
            href="/"
            className="text-sm text-teal-100 transition-colors hover:text-white"
          >
            Inicio
          </Link>
          <Link
            href="/sobre-nosotros"
            className="text-sm text-teal-100 transition-colors hover:text-white"
          >
            Sobre Nosotros
          </Link>
        </nav>
      </div>
    </footer>
  )
}
