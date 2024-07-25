import { About } from 'About'
import { AppBar, MainContainer } from 'components'
import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { Team } from 'Team'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AppBar />
      <Routes>
        <Route path="/" element={<MainContainer />} />
        <Route path="/about" element={<About />} />
        <Route path="/team" element={<Team />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
