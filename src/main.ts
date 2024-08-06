import 'assets/scss/app.scss'

document
    .querySelector<HTMLDivElement>('#app')!
    .innerHTML = `
  <div>
    <a href="https://vitejs.dev" target="_blank">
    </a>
    <p class="read-the-docs">
      Click on the Vite and TypeScript logos to learn more
    </p>
  </div>
`
