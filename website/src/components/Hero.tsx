import React, { useState } from 'react';
import { ArrowRightLeft, Hand, MessageCircle, Type } from 'lucide-react';

const Hero = () => {
  const [translationMode, setTranslationMode] = useState('asl-to-text');

  return (
    <section className="relative bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-orange-500/10 to-purple-600/10"></div>
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <h1 className="text-4xl lg:text-6xl font-bold leading-tight">
              Breaking Language
              <span className="bg-gradient-to-r from-orange-400 to-orange-500 bg-clip-text text-transparent block">
                Barriers
              </span>
              in India
            </h1>
            <p className="text-xl lg:text-2xl text-gray-300 leading-relaxed">
              Seamless translation between American Sign Language and text, empowering the deaf community across India with accessible communication.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105 shadow-lg">
                Try Translation
              </button>
              <button className="border-2 border-gray-600 text-gray-300 hover:bg-gray-800 hover:text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200">
                Learn More
              </button>
            </div>
          </div>

          <div className="relative">
            <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Translation Demo</h3>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setTranslationMode(translationMode === 'asl-to-text' ? 'text-to-asl' : 'asl-to-text')}
                    className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded-full text-sm transition-colors duration-200 flex items-center space-x-2 text-gray-300"
                  >
                    <span>{translationMode === 'asl-to-text' ? 'ASL → Text' : 'Text → ASL'}</span>
                    <ArrowRightLeft className="h-3 w-3" />
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-900 rounded-lg p-4 aspect-video flex items-center justify-center relative overflow-hidden border border-gray-700">
                  <div className="absolute inset-0 bg-gradient-to-br from-orange-500/20 to-purple-600/20"></div>
                  <div className="relative text-center">
                    {translationMode === 'asl-to-text' ? (
                      <>
                        <Hand className="h-12 w-12 mx-auto mb-2 text-orange-400" />
                        <p className="text-sm text-gray-400">ASL Input</p>
                      </>
                    ) : (
                      <>
                        <Type className="h-12 w-12 mx-auto mb-2 text-orange-400" />
                        <p className="text-sm text-gray-400">Text Input</p>
                      </>
                    )}
                  </div>
                </div>

                <div className="bg-gray-900 rounded-lg p-4 aspect-video flex items-center justify-center relative border border-gray-700">
                  <div className="text-center">
                    {translationMode === 'asl-to-text' ? (
                      <>
                        <Type className="h-12 w-12 mx-auto mb-2 text-orange-400" />
                        <div className="bg-gray-800 rounded-lg p-3 mt-2 border border-gray-600">
                          <p className="text-white font-medium">
                            "Hello, how are you today?"
                          </p>
                        </div>
                      </>
                    ) : (
                      <>
                        <Hand className="h-12 w-12 mx-auto mb-2 text-orange-400" />
                        <div className="bg-gray-800 rounded-lg p-3 mt-2 border border-gray-600">
                          <p className="text-white font-medium">
                            ASL Gestures
                          </p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-center">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 rounded-full bg-orange-400 animate-pulse"></div>
                  <div className="w-2 h-2 rounded-full bg-orange-400 animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 rounded-full bg-orange-400 animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                </div>
                <span className="ml-3 text-sm text-gray-400">
                  Ready to translate
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;