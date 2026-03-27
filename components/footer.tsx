import Image from "next/image"

export default function Footer() {
  return (
    <footer className="bg-neutral-800 py-12">
      <div className="mx-auto px-6 flex justify-between items-center" style={{ maxWidth: "1200px" }}>
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
        <nav className="flex justify-between gap-12">
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Inicio</a>
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Nosotros</a>
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Servicios</a>
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Contacto</a>
        </nav>
      </div>
    </footer>
  )
}
