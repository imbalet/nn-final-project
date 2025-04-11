import { useState } from 'react'
import './App.css'
import './components/Header.jsx'
import Header from './components/Header.jsx'
import './components/TextArea.jsx'
import Footer from './components/Footer.jsx'
import TextAreaWithButton from './components/TextAreaWithButton.jsx'
function App() {
  return (
    <div>
    <Header />

    <div className='paragraph'>
    <h2>Summary AI кратко перескажет видео c YouTube, а также даст список самых повторящихся слов</h2> 
      <TextAreaWithButton />
    </div>

    <Footer/>
    </div>
  )
}

export default App
