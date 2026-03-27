import Header from "@/components/header"
import Footer from "@/components/footer"

export default function Home() {
  return (
    <main>
      <Header />
      <section className="w-screen h-screen bg-teal-500">
      </section>

      <section className="bg-teal-100 py-16">
        <div className="mx-auto px-6" style={{ maxWidth: "1200px" }}>
          <div className="flex gap-12 items-center">
            <div className="flex-1 text-left">
              <h2 className="text-3xl font-bold mb-4">Título de sección</h2>
              <p className="text-base text-gray-700">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
            <div className="flex-1">
              <div className="w-full aspect-4/3 bg-teal-300 rounded-lg overflow-hidden">
                <img
                  src="https://placehold.co/800x600"
                  alt="Placeholder"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="bg-teal-300 py-16">
        <div className="mx-auto px-6 flex justify-center items-center" style={{ maxWidth: "1200px" }}>
          <p className="text-center text-base text-gray-700">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </p>
        </div>
      </section>
      <section className="bg-teal-100 py-16">
        <div className="mx-auto px-6" style={{ maxWidth: "1200px" }}>
          <div className="flex gap-12 items-center">
            <div className="flex-1">
              <div className="w-full aspect-4/3 bg-teal-300 rounded-lg overflow-hidden">
                <img
                  src="https://placehold.co/800x600"
                  alt="Placeholder"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
            <div className="flex-1 text-left">
              <h2 className="text-3xl font-bold mb-4">Título de sección</h2>
              <p className="text-base text-gray-700">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </main>
  )
}