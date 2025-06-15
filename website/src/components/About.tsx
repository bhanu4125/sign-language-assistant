import React from 'react';
import { Target, Users, Lightbulb, Heart } from 'lucide-react';

const About = () => {
  const sections = [
    {
      icon: Target,
      title: "Our Mission",
      subtitle: "What We Do",
      content: "We develop cutting-edge translation technology that provides seamless conversion between American Sign Language and text. Our platform breaks down communication barriers and creates inclusive environments for deaf and hard-of-hearing individuals across India.",
      color: "text-orange-500",
      bgColor: "bg-orange-500/10",
      borderColor: "border-orange-500/20"
    },
    {
      icon: Users,
      title: "Who We Serve",
      subtitle: "Our Community",
      content: "We serve the deaf community in India and globally, their families, educators, healthcare providers, businesses, and anyone committed to creating more inclusive and accessible communication experiences in the Indian subcontinent.",
      color: "text-teal-400",
      bgColor: "bg-teal-400/10",
      borderColor: "border-teal-400/20"
    },
    {
      icon: Heart,
      title: "Our Vision",
      subtitle: "Why We Exist",
      content: "To improve the lives of deaf people in India and worldwide by eliminating communication barriers. We envision a world where sign language is universally understood and accessible, fostering true inclusion and equality in Indian society.",
      color: "text-pink-400",
      bgColor: "bg-pink-400/10",
      borderColor: "border-pink-400/20"
    },
    {
      icon: Lightbulb,
      title: "Innovation Focus",
      subtitle: "How We Lead",
      content: "Through advanced translation technology and pattern recognition, we're pioneering solutions that understand the nuances of sign language. Our technology supports 200+ sign languages and continues to evolve with community feedback from India and beyond.",
      color: "text-purple-400",
      bgColor: "bg-purple-400/10",
      borderColor: "border-purple-400/20"
    }
  ];

  return (
    <section id="about" className="py-20 bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            About sign2text
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            We're on a mission to create a world where communication knows no barriers, 
            where every person in India can connect, learn, and thrive regardless of their hearing ability.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {sections.map((section, index) => {
            const IconComponent = section.icon;
            return (
              <div 
                key={index}
                className={`group bg-gray-800 rounded-2xl p-8 border ${section.borderColor} hover:border-opacity-50 transition-all duration-300 hover:shadow-lg`}
              >
                <div className="flex items-start space-x-6">
                  <div className={`${section.bgColor} ${section.color} w-16 h-16 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300 border ${section.borderColor}`}>
                    <IconComponent className="h-8 w-8" />
                  </div>
                  <div className="flex-1">
                    <div className="mb-3">
                      <p className={`text-sm font-medium ${section.color} uppercase tracking-wide`}>
                        {section.subtitle}
                      </p>
                      <h3 className="text-2xl font-bold text-white mt-1">
                        {section.title}
                      </h3>
                    </div>
                    <p className="text-gray-400 leading-relaxed">
                      {section.content}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="bg-gradient-to-r from-orange-600 to-purple-600 rounded-2xl p-8 lg:p-12 text-white text-center">
          <h3 className="text-3xl font-bold mb-4">Join Our Mission in India</h3>
          <p className="text-xl text-orange-100 mb-8 max-w-2xl mx-auto">
            Together, we can build a more inclusive India where sign language is understood everywhere, 
            empowering millions of people to communicate freely and confidently.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-orange-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold transition-colors duration-200">
              Partner With Us
            </button>
            <button className="border-2 border-white text-white hover:bg-white hover:text-orange-600 px-8 py-3 rounded-lg font-semibold transition-all duration-200">
              Support Our Cause
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;