import React from 'react';
import { Globe, Mail, MapPin, Phone, Facebook, Twitter, Linkedin, Github } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-black text-white border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-2">
            <div className="flex items-center mb-6">
              <Globe className="h-8 w-8 text-orange-500" />
              <span className="ml-2 text-2xl font-bold">sign2text</span>
            </div>
            <p className="text-gray-400 leading-relaxed mb-6 max-w-md">
              Breaking language barriers with sign language translation technology. 
              Empowering the deaf community in India and worldwide to communicate freely and inclusively.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-500 hover:text-orange-500 transition-colors duration-200">
                <Facebook className="h-6 w-6" />
              </a>
              <a href="#" className="text-gray-500 hover:text-orange-500 transition-colors duration-200">
                <Twitter className="h-6 w-6" />
              </a>
              <a href="#" className="text-gray-500 hover:text-orange-500 transition-colors duration-200">
                <Linkedin className="h-6 w-6" />
              </a>
              <a href="#" className="text-gray-500 hover:text-orange-500 transition-colors duration-200">
                <Github className="h-6 w-6" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-6 text-white">Quick Links</h3>
            <ul className="space-y-3">
              <li>
                <a href="#about" className="text-gray-400 hover:text-white transition-colors duration-200">
                  About Us
                </a>
              </li>
              <li>
                <a href="#asl-info" className="text-gray-400 hover:text-white transition-colors duration-200">
                  What is ASL?
                </a>
              </li>
              <li>
                <a href="#features" className="text-gray-400 hover:text-white transition-colors duration-200">
                  Features
                </a>
              </li>
              <li>
                <a href="#statistics" className="text-gray-400 hover:text-white transition-colors duration-200">
                  Statistics
                </a>
              </li>
              <li>
                <a href="#reviews" className="text-gray-400 hover:text-white transition-colors duration-200">
                  Reviews
                </a>
              </li>
              <li>
                <a href="#feedback" className="text-gray-400 hover:text-white transition-colors duration-200">
                  Feedback
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-6 text-white">Contact Us</h3>
            <div className="space-y-4">
              <div className="flex items-center">
                <Mail className="h-5 w-5 text-orange-500 mr-3" />
                <span className="text-gray-400">hello@sign2text.in</span>
              </div>
              <div className="flex items-center">
                <Phone className="h-5 w-5 text-orange-500 mr-3" />
                <span className="text-gray-400">+91 98765 43210</span>
              </div>
              <div className="flex items-start">
                <MapPin className="h-5 w-5 text-orange-500 mr-3 mt-1" />
                <span className="text-gray-400">
                  Tech Park, Sector 5<br />
                  Bangalore, Karnataka 560001<br />
                  India
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-500 text-sm">
              © 2024 sign2text. All rights reserved. Built with ❤️ for the deaf community in India.
            </p>
            <div className="mt-4 md:mt-0">
              <p className="text-gray-500 text-sm">
                Improving lives of deaf people across India and worldwide
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;