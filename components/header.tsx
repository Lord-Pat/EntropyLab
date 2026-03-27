export default function Header() {
  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-white/30 backdrop-blur-md border-b border-white/20">
      <div className="mx-auto px-6 h-16 flex items-center justify-between" style={{ maxWidth: "1200px" }}>
        <div className="text-xl font-bold text-teal-800">Logo</div>
        <nav className="flex items-center gap-8">
          <a href="#" className="text-sm font-medium text-teal-900 hover:text-teal-600 transition-colors">Inicio</a>
          <a href="#" className="text-sm font-medium text-teal-900 hover:text-teal-600 transition-colors">Nosotros</a>
          <a href="#" className="text-sm font-medium text-teal-900 hover:text-teal-600 transition-colors">Servicios</a>
          <a href="#" className="text-sm font-medium text-teal-900 hover:text-teal-600 transition-colors">Contacto</a>
        </nav>
      </div>
    </header>
  )
}
