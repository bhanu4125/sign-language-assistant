import React from 'react';
import { Zap, Shield, Smartphone, Users, Globe, ArrowRightLeft } from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: ArrowRightLeft,
      title: "Bidirectional Translation",
      description: "Seamless translation between ASL and text in both directions for complete communication flexibility in India.",
      color: "text-orange-500",
      bgColor: "bg-orange-500/10",
      borderColor: "border-orange-500/20"
    },
    {
      icon: Zap,
      title: "Real-Time Processing",
      description: "Instant translation with minimal latency for natural, flowing conversations and interactions across Indian communities.",
      color: "text-purple-400",
      bgColor: "bg-purple-400/10",
      borderColor: "border-purple-400/20"
    },
    {
      icon: Smartphone,
      title: "Cross-Platform Access",
      description: "Available on web, mobile, and desktop platforms for convenient access anywhere in India, anytime.",
      color: "text-blue-400",
      bgColor: "bg-blue-400/10",
      borderColor: "border-blue-400/20"
    },
    {
      icon: Globe,
      title: "200+ Sign Languages",
      description: "Support for major sign languages worldwide, with continuous expansion based on Indian community needs.",
      color: "text-green-400",
      bgColor: "bg-green-400/10",
      borderColor: "border-green-400/20"
    },
    {
      icon: Shield,
      title: "Privacy First",
      description: "End-to-end encryption and privacy-focused design to protect your conversations and personal data in India.",
      color: "text-red-400",
      bgColor: "bg-red-400/10",
      borderColor: "border-red-400/20"
    },
    {
      icon: Users,
      title: "Community Driven",
      description: "Built with and for the Indian deaf community, incorporating feedback and cultural understanding.",
      color: "text-teal-400",
      bgColor: "bg-teal-400/10",
      borderColor: "border-teal-400/20"
    }
  ];

  return (
    <section id="features" className="py-20 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Why Choose sign2text?
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Overcome language barriers and engage with people from diverse linguistic and cultural backgrounds across India, 
            wherever and whenever you need.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <div 
                key={index}
                className={`group bg-gray-900 rounded-2xl p-8 border ${feature.borderColor} hover:border-opacity-50 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2`}
              >
                <div className={`${feature.bgColor} ${feature.color} w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 border ${feature.borderColor}`}>
                  <IconComponent className="h-8 w-8" />
                </div>
                <h3 className={`text-xl font-bold text-white mb-3 group-hover:${feature.color} transition-colors duration-300`}>
                  {feature.title}
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>

        <div className="mt-16 bg-gray-900 rounded-2xl p-8 lg:p-12 border border-gray-800">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">
              Experience the Future of Communication in India
            </h3>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Join thousands of users who are already breaking down communication barriers with our translation technology across India.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors duration-200">
              Start Free Trial
            </button>
            <button className="border-2 border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-white px-8 py-3 rounded-lg font-semibold transition-all duration-200">
              View Pricing
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;