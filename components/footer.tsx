import Image from "next/image"

export default function Footer() {
  return (
    <footer className="bg-neutral-800 py-12">
      <div
        className="mx-auto flex flex-col items-start gap-8 px-4 sm:px-6 md:flex-row md:items-center md:justify-between"
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

        <nav className="flex flex-wrap gap-4 sm:gap-8 md:justify-end">
          <a href="#" className="text-sm text-teal-100 transition-colors hover:text-white">
            Inicio
          </a>
          <a href="#" className="text-sm text-teal-100 transition-colors hover:text-white">
            Nosotros
          </a>
          <a href="#" className="text-sm text-teal-100 transition-colors hover:text-white">
            Servicios
          </a>
          <a href="#" className="text-sm text-teal-100 transition-colors hover:text-white">
            Contacto
          </a>
        </nav>
      </div>
    </footer>
  )
}
