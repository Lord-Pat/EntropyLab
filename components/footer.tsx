import Image from "next/image"
import Link from "next/link"

export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-black/60 py-4 backdrop-blur-md">
      <div
        className="mx-auto flex flex-row items-center justify-between px-4 sm:px-6"
        style={{ maxWidth: "1200px" }}
      >
        <Link href="/" className="flex items-center gap-2">
          <Image
            src="/lava lamp logo.png"
            alt="EntropyLab logo"
            width={28}
            height={28}
            className="h-7 w-7 object-contain invert"
          />
          <div className="text-base font-bold tracking-tight text-white">
            Entropy<span className="text-red-600">Lab</span>
          </div>
        </Link>

        <nav className="flex items-center gap-6">
          <Link
            href="/"
            className="text-xs text-teal-100 transition-colors hover:text-white"
          >
            Inicio
          </Link>
          <Link
            href="/sobre-nosotros"
            className="text-xs text-teal-100 transition-colors hover:text-white"
          >
            Sobre Nosotros
          </Link>
        </nav>
      </div>
    </footer>
  )
}
