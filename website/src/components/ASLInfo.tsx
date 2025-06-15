import React from 'react';
import { BookOpen, Globe, Users, Clock, Languages, Eye } from 'lucide-react';

const ASLInfo = () => {
  const aslFacts = [
    {
      icon: Users,
      title: "500,000+ Users",
      description: "More than half a million people throughout the US use ASL as their native language"
    },
    {
      icon: Languages,
      title: "3rd Most Used",
      description: "ASL is the third most commonly used language in the United States, after English and Spanish"
    },
    {
      icon: Globe,
      title: "Not Universal",
      description: "There are over 300 different sign languages worldwide, each unique to its region"
    },
    {
      icon: Eye,
      title: "Visual Language",
      description: "ASL uses body movements and visual components rather than sound for communication"
    }
  ];

  return (
    <section id="asl-info" className="py-20 bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            What Is American Sign Language (ASL)?
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Understanding the rich history and unique characteristics of American Sign Language
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          <div className="bg-gray-800 rounded-2xl p-8 border border-gray-700">
            <div className="flex items-center mb-6">
              <BookOpen className="h-8 w-8 text-orange-500 mr-3" />
              <h3 className="text-2xl font-bold text-white">About ASL</h3>
            </div>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <p>
                ASL, short for American Sign Language, is the sign language most commonly used by the Deaf and Hard of Hearing people in the United States.
              </p>
              <p>
                Approximately more than a half-million people throughout the US use ASL to communicate as their native language. ASL is the third most commonly used language in the United States, after English and Spanish.
              </p>
              <p>
                Contrary to popular belief, ASL is not representative of English nor is it some sort of imitation of spoken English that we use on a day-to-day basis. For many, it will come as a great surprise that ASL has more similarities to spoken Japanese and Navajo than to English.
              </p>
            </div>
          </div>

          <div className="bg-gray-800 rounded-2xl p-8 border border-gray-700">
            <div className="flex items-center mb-6">
              <Eye className="h-8 w-8 text-orange-500 mr-3" />
              <h3 className="text-2xl font-bold text-white">Visual Language</h3>
            </div>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <p>
                When we discuss ASL or any other type of sign language, we are referring to what is called a visual language. The visual component refers to the use of body movements versus sound.
              </p>
              <p>
                Because "listeners" must use their eyes to "receive" the information, this language was specifically created to be easily recognized by the eyes. The visual component refers to the body movements or signs that are performed to convey a message.
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {aslFacts.map((fact, index) => {
            const IconComponent = fact.icon;
            return (
              <div key={index} className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-orange-500 transition-colors duration-300">
                <IconComponent className="h-10 w-10 text-orange-500 mb-4" />
                <h4 className="text-lg font-bold text-white mb-2">{fact.title}</h4>
                <p className="text-gray-400 text-sm">{fact.description}</p>
              </div>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div className="bg-gray-800 rounded-2xl p-8 border border-gray-700">
            <div className="flex items-center mb-6">
              <Clock className="h-8 w-8 text-orange-500 mr-3" />
              <h3 className="text-2xl font-bold text-white">A Brief History of ASL</h3>
            </div>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <p>
                ASL is a relatively new language, which first appeared in the 1800s with the founding of the first successful American School for the Deaf by Thomas Hopkins Gallaudet and Laurent Clerc (first Deaf Teacher from France) in 1817.
              </p>
              <p>
                With strong roots in French Sign Language, ASL evolved to incorporate the signs students would use in less formal settings such as in their home or within the deaf community.
              </p>
              <p>
                As students graduated from the American School for the Deaf, some went on to open their own schools, passing along this evolving American Sign Language as the contact language for the deaf in the United States.
              </p>
            </div>
          </div>

          <div className="bg-gray-800 rounded-2xl p-8 border border-gray-700">
            <div className="flex items-center mb-6">
              <Globe className="h-8 w-8 text-orange-500 mr-3" />
              <h3 className="text-2xl font-bold text-white">Is There a Universal Sign Language?</h3>
            </div>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <p>
                There is no universal language for the deaf – all over the world, different sign languages have developed that vary from one another. According to the World Federation of the Deaf, there are over 300 signed languages in the world.
              </p>
              <p>
                A spoken English speaker from the USA, for example, can generally understand someone from another English-speaking nation such as England or Australia.
              </p>
              <p>
                But with sign language, someone who signs using American Sign language would not be able to understand someone who signs using British Sign Language (BSL) or even Australian (Auslan).
              </p>
            </div>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500 italic">
            Reference: Mitchell, Ross E., et al. (2006). How Many People Use ASL in the United States? Gallaudet University, Gallaudet Research Institute, Washington, D.C.
          </p>
        </div>
      </div>
    </section>
  );
};

export default ASLInfo;