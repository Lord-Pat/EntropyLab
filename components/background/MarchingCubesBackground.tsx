"use client"

import { useEffect, useRef } from "react"

export default function MarchingCubesBackground() {
  const mountRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let mounted = true
    let animationId: number

    const init = async () => {
      const THREE = await import("three")
      const { MarchingCubes } = await import(
        "three/examples/jsm/objects/MarchingCubes.js"
      )

      const mount = mountRef.current
      if (!mount || !mounted) return

      const scene = new THREE.Scene()

      const camera = new THREE.PerspectiveCamera(
        45,
        window.innerWidth / window.innerHeight,
        1,
        10000
      )
      camera.position.set(0, 0, 500)

      // Luces más intensas para aspecto brillante
      const ambientLight = new THREE.AmbientLight(0x111111)
      scene.add(ambientLight)

      const directionalLight = new THREE.DirectionalLight(0xffffff, 3)
      directionalLight.position.set(0.5, 1, 1)
      scene.add(directionalLight)

      // Punto de luz principal (rojo-naranja, sigue a los blobs)
      const pointLight = new THREE.PointLight(0xff4400, 6, 0)
      scene.add(pointLight)

      // Segundo punto de luz para dar profundidad
      const pointLight2 = new THREE.PointLight(0xff0000, 3, 0)
      pointLight2.position.set(-200, -200, 200)
      scene.add(pointLight2)

      // Material más vivo y brillante
      const material = new THREE.MeshPhongMaterial({
        color: 0xff2200,
        emissive: 0x550000,
        specular: 0xffffff,
        shininess: 150,
      })

      const resolution = 28
      const effect = new MarchingCubes(resolution, material, true, true, 100000)
      effect.position.set(0, 0, 0)
      effect.scale.set(300, 300, 300)
      effect.enableUvs = false
      effect.enableColors = false
      scene.add(effect)

      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false })
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
      renderer.setSize(window.innerWidth, window.innerHeight)
      renderer.setClearColor(0x050505, 1)
      mount.appendChild(renderer.domElement)

      const numBlobs = 10
      const updateCubes = (t: number) => {
        effect.reset()
        const subtract = 12
        const strength = 1.2 / ((Math.sqrt(numBlobs) - 1) / 4 + 1)

        for (let i = 0; i < numBlobs; i++) {
          const ballx =
            Math.sin(i + 1.26 * t * (1.03 + 0.5 * Math.cos(0.21 * i))) * 0.27 + 0.5
          const bally =
            Math.abs(Math.cos(i + 1.12 * t * Math.cos(1.22 + 0.1424 * i))) * 0.77
          const ballz =
            Math.cos(i + 1.32 * t * 0.1 * Math.sin(0.92 + 0.53 * i)) * 0.27 + 0.5
          effect.addBall(ballx, bally, ballz, strength, subtract)
        }
        effect.update()
      }

      let lastTime = performance.now()
      let time = 0

      const animate = () => {
        if (!mounted) return
        animationId = requestAnimationFrame(animate)

        const now = performance.now()
        time += ((now - lastTime) / 1000) * 0.4
        lastTime = now

        pointLight.position.set(
          Math.sin(time * 0.7) * 300,
          Math.cos(time * 0.5) * 400,
          Math.cos(time * 0.3) * 300
        )
        pointLight2.position.set(
          Math.cos(time * 0.4) * 250,
          Math.sin(time * 0.6) * 250,
          Math.sin(time * 0.2) * 200
        )

        updateCubes(time)
        renderer.render(scene, camera)
      }

      animate()

      const handleResize = () => {
        camera.aspect = window.innerWidth / window.innerHeight
        camera.updateProjectionMatrix()
        renderer.setSize(window.innerWidth, window.innerHeight)
      }
      window.addEventListener("resize", handleResize)

      return () => {
        window.removeEventListener("resize", handleResize)
        cancelAnimationFrame(animationId)
        renderer.dispose()
        if (mount.contains(renderer.domElement)) {
          mount.removeChild(renderer.domElement)
        }
      }
    }

    let cleanupFn: (() => void) | undefined
    init().then((fn) => {
      cleanupFn = fn
    })

    return () => {
      mounted = false
      cancelAnimationFrame(animationId)
      cleanupFn?.()
    }
  }, [])

  return (
    <div
      ref={mountRef}
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        zIndex: -1,
        pointerEvents: "none",
      }}
    />
  )
}
