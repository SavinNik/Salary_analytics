import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Header } from './components/Header'
import { FormSend } from './components/FormSend'



function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <Header></Header>
    <FormSend></FormSend>
    </>
  )
}

export default App
