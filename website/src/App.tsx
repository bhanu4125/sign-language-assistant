import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Statistics from './components/Statistics';
import About from './components/About';
import ASLInfo from './components/ASLInfo';
import Features from './components/Features';
import Reviews from './components/Reviews';
import Feedback from './components/Feedback';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-black">
      <Header />
      <Hero />
      <Statistics />
      <About />
      <ASLInfo />
      <Features />
      <Reviews />
      <Feedback />
      <Footer />
    </div>
  );
}

export default App;