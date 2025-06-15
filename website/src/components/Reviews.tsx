import React from 'react';
import { Star, Quote, Users, Briefcase, GraduationCap } from 'lucide-react';

const Reviews = () => {
  const testimonials = [
    {
      name: "Dr. Priya Sharma",
      role: "Deaf Education Specialist",
      organization: "Indian Institute of Special Education",
      avatar: "PS",
      rating: 5,
      content: "sign2text has revolutionized how we communicate in our classroom in Mumbai. The accuracy and speed of translation has made education more accessible for our deaf students across India.",
      icon: GraduationCap,
      color: "text-orange-500"
    },
    {
      name: "Rajesh Kumar",
      role: "Accessibility Director",
      organization: "Tech Mahindra",
      avatar: "RK",
      rating: 5,
      content: "Implementing sign2text in our Bangalore office has created truly inclusive meetings. Our deaf employees now participate fully in all discussions and feel more connected to the team.",
      icon: Briefcase,
      color: "text-green-400"
    },
    {
      name: "Anita Desai",
      role: "Community Leader",
      organization: "Delhi Deaf Rights Coalition",
      avatar: "AD",
      rating: 5,
      content: "Finally, a technology that understands the nuances of sign language and works well in the Indian context. This isn't just translation - it's cultural bridge-building at its finest.",
      icon: Users,
      color: "text-purple-400"
    }
  ];

  return (
    <section id="reviews" className="py-20 bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Trusted by Communities Across India
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            See what our users and community leaders are saying about the impact of sign2text 
            on communication and accessibility in India.
          </p>
        </div>

        {/* Testimonials Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => {
            const IconComponent = testimonial.icon;
            return (
              <div key={index} className="bg-gray-800 rounded-2xl p-8 border border-gray-700 hover:border-gray-600 transition-all duration-300 relative">
                <div className="absolute top-6 right-6">
                  <Quote className="h-8 w-8 text-gray-600" />
                </div>
                
                <div className="flex items-center mb-6">
                  <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                    {testimonial.avatar}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-white">{testimonial.name}</h4>
                    <p className="text-sm text-gray-400">{testimonial.role}</p>
                    <p className={`text-sm ${testimonial.color}`}>{testimonial.organization}</p>
                  </div>
                  <IconComponent className={`h-6 w-6 ${testimonial.color}`} />
                </div>

                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-orange-400 fill-current" />
                  ))}
                </div>

                <p className="text-gray-300 leading-relaxed italic">
                  "{testimonial.content}"
                </p>
              </div>
            );
          })}
        </div>

        <div className="mt-16 text-center">
          <div className="bg-gray-800 rounded-2xl p-8 inline-block border border-gray-700">
            <div className="flex items-center justify-center space-x-8 text-gray-400">
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-500">98%</div>
                <div className="text-sm">User Satisfaction</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400">50K+</div>
                <div className="text-sm">Active Users</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400">24/7</div>
                <div className="text-sm">Support Available</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Reviews;