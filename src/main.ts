import 'assets/scss/app.scss'
console.log("+++++++++++++++++++++++++++++++++++++++++")
document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    <a href="https://vitejs.dev" target="_blank">
    </a>
    <p class="read-the-docs">
      Click on the Vite and TypeScript logos to learn more
    </p>
  </div>
`
// const server = Bun.serve({
//     port: 3000,
//     fetch(req) {
//         console.log("Bun! ", req)
//         return new Response("Bun!")
//     }
// })
//
// console.log(`Listening on http://localhost:${server.port} ...`)