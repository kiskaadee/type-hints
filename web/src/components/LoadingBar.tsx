import React from 'react'

interface LoadingBarProps {
  isLoading: boolean
}

export const LoadingBar: React.FC<LoadingBarProps> = ({ isLoading }) => {
  if (!isLoading) return null

  return (
    <div className="fixed top-0 left-0 right-0 h-[2px] z-50 overflow-hidden bg-black/40">
      <div className="h-full bg-gradient-to-r from-[#ffb000] via-[#10b981] to-[#ffb000] w-1/3 animate-[loading-slide_1.2s_ease-in-out_infinite]" />
      <style>{`
        @keyframes loading-slide {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(350%); }
        }
      `}</style>
    </div>
  )
}
