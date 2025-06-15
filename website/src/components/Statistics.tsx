import React, { useEffect, useState } from 'react';
import { Users, BookOpen, DollarSign, Building, Globe } from 'lucide-react';

const Statistics = () => {
  const [counts, setCounts] = useState({
    deafPeople: 0,
    marketValue: 0,
    languages: 0,
    enterprises: 0
  });

  useEffect(() => {
    const targetCounts = {
      deafPeople: 70000000,
      marketValue: 33.7,
      languages: 200,
      enterprises: 3
    };

    const duration = 2000;
    const steps = 60;
    const stepDuration = duration / steps;

    let currentStep = 0;
    const timer = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;
      
      setCounts({
        deafPeople: Math.floor(targetCounts.deafPeople * progress),
        marketValue: Math.floor(targetCounts.marketValue * progress * 10) / 10,
        languages: Math.floor(targetCounts.languages * progress),
        enterprises: Math.floor(targetCounts.enterprises * progress)
      });

      if (currentStep >= steps) {
        clearInterval(timer);
        setCounts(targetCounts);
      }
    }, stepDuration);

    return () => clearInterval(timer);
  }, []);

  const stats = [
    {
      icon: Users,
      title: "Deaf People Worldwide",
      value: `${(counts.deafPeople / 1000000).toFixed(0)}M`,
      description: "Globally there are 70 million deaf people. By 2050, over 700 million people could have disabling hearing loss.",
      color: "text-orange-500",
      bgColor: "bg-orange-500/10",
      borderColor: "border-orange-500/20"
    },
    {
      icon: BookOpen,
      title: "Literacy Challenge",
      value: "20-50%",
      description: "Spoken language literacy rates among deaf individuals are uncertain, with estimates ranging from 20% to 50%.",
      color: "text-blue-400",
      bgColor: "bg-blue-400/10",
      borderColor: "border-blue-400/20"
    },
    {
      icon: DollarSign,
      title: "Global Market Value",
      value: `$${counts.marketValue}B`,
      description: "The U.S. sign language translation market is worth $11B, with a global estimate of $33.7B across 30 developed nations.",
      color: "text-green-400",
      bgColor: "bg-green-400/10",
      borderColor: "border-green-400/20"
    },
    {
      icon: Building,
      title: "Enterprise Partners",
      value: `${counts.enterprises}x 1M+`,
      description: "Our technology is being reviewed by three enterprises, each with over 1 million retail customers.",
      color: "text-purple-400",
      bgColor: "bg-purple-400/10",
      borderColor: "border-purple-400/20"
    },
    {
      icon: Globe,
      title: "Languages Supported",
      value: `${counts.languages}+`,
      description: "Our translation solution currently partially supports 43 of the 200+ major sign languages to some extent, with exciting plans to expand further.",
      color: "text-teal-400",
      bgColor: "bg-teal-400/10",
      borderColor: "border-teal-400/20"
    }
  ];

  return (
    <section id="statistics" className="py-20 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Transforming Lives Through Translation
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Our mission is backed by compelling statistics that highlight the urgent need for accessible sign language translation technology in India and worldwide.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {stats.map((stat, index) => {
            const IconComponent = stat.icon;
            return (
              <div 
                key={index} 
                className={`bg-gray-900 rounded-2xl p-8 border ${stat.borderColor} hover:border-opacity-50 transition-all duration-300 transform hover:-translate-y-1`}
              >
                <div className={`${stat.bgColor} ${stat.color} w-16 h-16 rounded-xl flex items-center justify-center mb-6 border ${stat.borderColor}`}>
                  <IconComponent className="h-8 w-8" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">{stat.title}</h3>
                <div className={`text-4xl font-bold ${stat.color} mb-4`}>
                  {stat.value}
                </div>
                <p className="text-gray-400 leading-relaxed">{stat.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Statistics;