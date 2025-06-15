import React, { useState } from 'react';
import { Menu, X, Globe, MessageSquare } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-gray-900 shadow-lg border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <Globe className="h-8 w-8 text-orange-500" />
              <span className="ml-2 text-xl font-bold text-white">sign2text</span>
            </div>
          </div>

          <nav className="hidden md:flex space-x-8">
            <a href="#about" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">About</a>
            <a href="#asl-info" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">What is ASL?</a>
            <a href="#features" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Features</a>
            <a href="#statistics" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Statistics</a>
            <a href="#reviews" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Reviews</a>
            <a href="#feedback" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Feedback</a>
            <a href="#contact" className="text-orange-500 hover:text-orange-400 font-medium transition-colors duration-200">Contact</a>
          </nav>

          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-md text-gray-300 hover:text-orange-500 hover:bg-gray-800 transition-colors duration-200"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-800">
            <div className="flex flex-col space-y-4">
              <a href="#about" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">About</a>
              <a href="#asl-info" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">What is ASL?</a>
              <a href="#features" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Features</a>
              <a href="#statistics" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Statistics</a>
              <a href="#reviews" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Reviews</a>
              <a href="#feedback" className="text-gray-300 hover:text-orange-500 transition-colors duration-200">Feedback</a>
              <a href="#contact" className="text-orange-500 hover:text-orange-400 font-medium transition-colors duration-200">Contact</a>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;