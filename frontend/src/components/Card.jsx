import React from 'react';

const Card = ({ title, children, className = '' }) => {
  return (
    <div className={`bg-white shadow rounded-lg p-4 sm:p-6 ${className}`}>
      {title && (
        <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
          {title}
        </h3>
      )}
      <div>
        {children}
      </div>
    </div>
  );
};

export default Card; 