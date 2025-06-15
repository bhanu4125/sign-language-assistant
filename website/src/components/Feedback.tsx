import React, { useState } from 'react';
import { MessageSquare, Send, Star, ThumbsUp, AlertCircle } from 'lucide-react';

const Feedback = () => {
  const [feedback, setFeedback] = useState({
    name: '',
    email: '',
    rating: 5,
    category: 'general',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle feedback submission here
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFeedback({
      ...feedback,
      [e.target.name]: e.target.value
    });
  };

  const categories = [
    { value: 'general', label: 'General Feedback' },
    { value: 'feature', label: 'Feature Request' },
    { value: 'bug', label: 'Bug Report' },
    { value: 'translation', label: 'Translation Quality' },
    { value: 'accessibility', label: 'Accessibility' },
    { value: 'support', label: 'Support' }
  ];

  return (
    <section id="feedback" className="py-20 bg-black">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Share Your Feedback
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Help us improve sign2text for the Indian deaf community. Your feedback drives our innovation and helps us serve you better.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Feedback Form */}
          <div className="lg:col-span-2">
            <div className="bg-gray-900 rounded-2xl p-8 border border-gray-800">
              <div className="flex items-center mb-6">
                <MessageSquare className="h-6 w-6 text-orange-500 mr-3" />
                <h3 className="text-2xl font-bold text-white">Send Us Your Feedback</h3>
              </div>

              {submitted && (
                <div className="mb-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg flex items-center">
                  <ThumbsUp className="h-5 w-5 text-green-400 mr-3" />
                  <p className="text-green-400">Thank you for your feedback! We'll review it soon.</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                      Name
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={feedback.name}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200"
                      required
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={feedback.email}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="category" className="block text-sm font-medium text-gray-300 mb-2">
                      Category
                    </label>
                    <select
                      id="category"
                      name="category"
                      value={feedback.category}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200"
                    >
                      {categories.map((category) => (
                        <option key={category.value} value={category.value}>
                          {category.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Rating
                    </label>
                    <div className="flex items-center space-x-2 py-3">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          type="button"
                          onClick={() => setFeedback({ ...feedback, rating: star })}
                          className="focus:outline-none"
                        >
                          <Star
                            className={`h-6 w-6 ${
                              star <= feedback.rating
                                ? 'text-orange-400 fill-current'
                                : 'text-gray-600'
                            } hover:text-orange-400 transition-colors duration-200`}
                          />
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-300 mb-2">
                    Your Feedback
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={feedback.message}
                    onChange={handleInputChange}
                    rows={6}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200 resize-none"
                    placeholder="Tell us about your experience, suggestions, or any issues you've encountered..."
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200 flex items-center justify-center"
                >
                  <Send className="h-5 w-5 mr-2" />
                  Send Feedback
                </button>
              </form>
            </div>
          </div>

          {/* Feedback Info */}
          <div className="space-y-6">
            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800">
              <h4 className="text-lg font-bold text-white mb-4">Why Your Feedback Matters</h4>
              <ul className="space-y-3 text-gray-400">
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span>Helps us improve translation accuracy for Indian sign languages</span>
                </li>
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span>Guides our feature development priorities</span>
                </li>
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span>Ensures cultural sensitivity and accessibility</span>
                </li>
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span>Builds a stronger community platform</span>
                </li>
              </ul>
            </div>

            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800">
              <div className="flex items-center mb-4">
                <AlertCircle className="h-5 w-5 text-blue-400 mr-2" />
                <h4 className="text-lg font-bold text-white">Quick Response</h4>
              </div>
              <p className="text-gray-400 text-sm">
                We typically respond to feedback within 24-48 hours. For urgent issues, please contact our support team directly.
              </p>
            </div>

            <div className="bg-gradient-to-r from-orange-500/10 to-purple-600/10 rounded-2xl p-6 border border-orange-500/20">
              <h4 className="text-lg font-bold text-white mb-2">Community Impact</h4>
              <p className="text-gray-400 text-sm">
                Your feedback has helped us improve translation accuracy by 15% and add support for 5 new regional sign language variations in India.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Feedback;