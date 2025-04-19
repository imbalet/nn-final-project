import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'
import './components/Header.jsx'
import Header from './components/Header.jsx'
import './components/TextArea.jsx'
import Footer from './components/Footer.jsx'
import TextAreaWithButton from './components/TextAreaWithButton.jsx'
import Summary from './pages/Summary.jsx'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home/>} />
      <Route path="/summary" element={<Summary />} />
    </Routes>
  )
}

function Home(){
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
