"use client";

import React, { useState } from 'react';
import { Search, Rocket, Zap, Shield, Target, Loader2, Sparkles, TrendingUp, ChevronRight, User } from 'lucide-react';

const Card = ({ item }: { item: any }) => {
  const matchScore = item.match_score || 0;
  return (
    <article className="glass-morphism p-6 rounded-2xl border border-white/10 hover:border-accent/50 transition-all duration-300 group">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1 pr-2">
          <div className="flex items-center gap-2 mb-1">
            {matchScore > 90 && <Zap className="text-yellow-400 w-4 h-4 fill-yellow-400" />}
            <span className="text-[10px] uppercase tracking-[0.2em] font-bold text-accent">Niche Opportunity</span>
          </div>
          <h3 className="text-lg font-bold text-white group-hover:text-accent transition-colors leading-tight">{item.idea || "Untitled Opportunity"}</h3>
        </div>
        <div className="px-3 py-1 bg-white/5 rounded-full border border-white/10 whitespace-nowrap">
          <span className="text-xs font-bold text-accent">{matchScore}% Match</span>
        </div>
      </div>
      <div className="space-y-4">
        <div>
          <h4 className="text-[10px] uppercase tracking-widest text-gray-500 mb-1.5 flex items-center gap-1">
            <User className="w-3 h-3" /> Competitive Advantage
          </h4>
          <p className="text-gray-300 text-sm leading-relaxed line-clamp-4">{item.reason}</p>
        </div>
        <div>
          <h4 className="text-[10px] uppercase tracking-widest text-gray-500 mb-1.5 flex items-center gap-1">
            <TrendingUp className="w-3 h-3" /> Profitability
          </h4>
          <p className="text-gray-300 text-sm font-medium">{item.profitability}</p>
        </div>
      </div>
      <div className="mt-6 flex justify-end">
         <button className="text-[11px] font-bold uppercase tracking-widest text-accent flex items-center gap-1 group/btn hover:brightness-125 transition-all">
            In-depth Analysis <ChevronRight className="w-3 h-3 group-hover/btn:translate-x-1 transition-transform" />
         </button>
      </div>
    </article>
  );
};

export default function Home() {
  const [topic, setTopic] = useState('');
  const [userProfile, setUserProfile] = useState('- Expert in C++, Python, and 3D Modeling\n- Experience in high-performance computing\n- Developed desktop applications with complex algos');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDiscover = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('/api/discover', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, userProfile }),
      });

      if (!response.ok) {
        throw new Error('Agent failed to process the request. Please check if the backend is ready.');
      }

      const res = await response.json();
      if (res.error) throw new Error(res.error);
      setResults(res.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark text-white selection:bg-accent/30 selection:text-white pb-20 overflow-x-hidden">
      {/* Background decoration */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-accent/10 blur-[150px] rounded-full"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-500/10 blur-[150px] rounded-full"></div>
      </div>

      <main className="max-w-6xl mx-auto px-6 pt-24">
        {/* Header - Optimized for SEO with semantic H1 */}
        <section className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8 animate-pulse">
            <Sparkles className="w-4 h-4 text-accent" />
            <span className="text-[11px] uppercase tracking-[3px] font-bold text-white/70">Intelligence Engine v1.0</span>
          </div>
          <h1 className="text-6xl md:text-8xl font-black mb-8 tracking-tighter leading-none">
            NICHE <span className="gold-gradient">EXPLORER</span>
          </h1>
          <p className="text-gray-500 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed font-medium">
            AI-powered discovery for technical entrepreneurs. Find high-moat project ideas by analyzing internet-scale pain points.
          </p>
        </section>

        {/* User Profile Input Section */}
        <section className="max-w-3xl mx-auto mb-8 animate-in fade-in slide-in-from-top-4 duration-700">
           <div className="glass-morphism rounded-2xl border border-white/10 p-6">
              <label htmlFor="user-profile" className="flex items-center gap-2 text-[10px] uppercase tracking-[0.2em] font-bold text-accent mb-4">
                <User className="w-4 h-4" /> My Technical Identity & Skills
              </label>
              <textarea
                id="user-profile"
                value={userProfile}
                onChange={(e) => setUserProfile(e.target.value)}
                placeholder="List your expertises (e.g. 'C++, React, ML, Distributed systems...')"
                className="w-full bg-black/40 border border-white/5 rounded-xl p-4 text-gray-300 text-sm focus:outline-none focus:border-accent/40 transition-colors min-h-[120px] resize-none"
              />
           </div>
        </section>

        {/* Search Bar */}
        <section className="relative max-w-3xl mx-auto mb-24 group">
          <div className="absolute -inset-1 bg-linear-to-r from-accent to-blue-600 rounded-3xl blur-xl opacity-20 group-hover:opacity-40 transition-opacity duration-1000"></div>
          <form onSubmit={handleDiscover} className="relative flex items-center bg-[#111] border border-white/10 rounded-2xl p-2.5 pl-7 focus-within:border-accent/40 focus-within:ring-1 focus-within:ring-accent/40 transition-all duration-300">
            <label htmlFor="topic-search" className="sr-only">Search for a niche</label>
            <Search className="text-gray-500 w-6 h-6 mr-4" />
            <input
              id="topic-search"
              type="text"
              placeholder="Target Market (e.g. '3D Printing', 'CAD tools'...)"
              className="bg-transparent flex-1 outline-none text-xl placeholder:text-gray-700 py-3"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              disabled={loading}
              required
            />
            <button
              type="submit"
              disabled={loading || !topic}
              className="relative overflow-hidden bg-accent hover:opacity-90 active:scale-95 text-black font-black uppercase text-[13px] tracking-widest px-10 py-5 rounded-xl transition-all flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed group/launch"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Rocket className="w-5 h-5 group-hover/launch:-translate-y-1 transition-transform" />}
              {loading ? "Analyzing..." : "Launch Miner"}
            </button>
          </form>
        </section>

        {/* Error State */}
        {error && (
          <div className="max-w-xl mx-auto bg-red-500/10 border border-red-500/20 text-red-500 p-6 rounded-2xl text-center mb-16 flex flex-col items-center gap-3" role="alert">
            <span className="font-bold uppercase tracking-widest text-xs">Extraction Failed</span>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="space-y-16 animate-in fade-in slide-in-from-bottom-5 duration-1000">
            <header className="flex flex-col md:flex-row md:items-end justify-between border-b border-white/10 pb-8 gap-4">
              <div>
                <h2 className="text-4xl font-black flex items-center gap-4 tracking-tight">
                  <Target className="text-accent w-10 h-10" /> OPPORTUNITIES
                </h2>
                <p className="text-gray-500 mt-2 font-medium">Curated niches with high technical alignment</p>
              </div>
              <div className="bg-white/5 border border-white/10 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-widest text-gray-400">
                Processed <span className="text-accent">{results.evaluated_ideas?.length || 0}</span> Core Insights
              </div>
            </header>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {results.evaluated_ideas?.map((item: any, index: number) => (
                <Card key={index} item={item} />
              ))}
            </div>

            {/* Strategic Summary */}
            <section className="relative group mt-32">
              <div className="absolute -inset-1 bg-linear-to-b from-white/10 to-transparent rounded-[3rem] blur-sm opacity-50"></div>
              <div className="relative glass-morphism p-12 md:p-20 rounded-[3rem] border border-white/10">
                <div className="max-w-3xl">
                  <h3 className="text-4xl font-black mb-8 flex items-center gap-4 tracking-tight">
                    <Shield className="text-accent w-10 h-10" /> STRATEGIC <span className="text-white/40">REPORT</span>
                  </h3>
                  <div className="text-gray-400 text-lg leading-relaxed space-y-6">
                    {results.final_report.split('\n').map((line: string, i: number) => (
                      line.trim() && <p key={i}>{line}</p>
                    ))}
                  </div>
                </div>
              </div>
            </section>
          </div>
        )}

        {/* Features Info - Good for SEO keywords */}
        {!results && !loading && (
          <section className="grid grid-cols-1 md:grid-cols-3 gap-12 mt-20 opacity-40 hover:opacity-100 transition-opacity duration-700">
             <div className="p-8 rounded-3xl border border-dashed border-white/10 group">
                <Target className="text-gray-600 mb-6 group-hover:text-accent transition-colors" />
                <h4 className="font-bold text-lg mb-3">Ultra Precision Mining</h4>
                <p className="text-sm text-gray-500 leading-relaxed font-medium">Deep-scans developer communities like Reddit and HackerNews for unspoken frustrations and tool gaps.</p>
             </div>
             <div className="p-8 rounded-3xl border border-dashed border-white/10 group">
                <TrendingUp className="text-gray-600 mb-6 group-hover:text-accent transition-colors" />
                <h4 className="font-bold text-lg mb-3">Economic Arbitrage</h4>
                <p className="text-sm text-gray-500 leading-relaxed font-medium">Identifies high contract value potentials in scientific and industrial domains underserved by mainstream tech.</p>
             </div>
             <div className="p-8 rounded-3xl border border-dashed border-white/10 group">
                <Shield className="text-gray-600 mb-6 group-hover:text-accent transition-colors" />
                <h4 className="font-bold text-lg mb-3">Algorithmic Moat</h4>
                <p className="text-sm text-gray-500 leading-relaxed font-medium">Specifically filters for niches requiring C++ and Geometric Algorithm expertise to build defensible businesses.</p>
             </div>
          </section>
        )}
      </main>

      <footer className="mt-32 border-t border-white/5 py-12 text-center">
        <div className="text-gray-600 text-[10px] uppercase tracking-[0.4em] font-bold">
          &copy; MMXXVI NICHE EXPLORER PRO &bull; ADVANCED MARKET MINING
        </div>
      </footer>
    </div>
  );
}
