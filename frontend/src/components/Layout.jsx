import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

const Layout = () => {
  const navLinkClass = ({ isActive }) => 
    `px-3 py-2 rounded-md text-sm font-medium ${isActive ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700'}`;

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center text-xl font-bold text-gray-800">
                Fake News Dashboard
              </div>
            </div>
            <div className="flex items-center">
              <div className="hidden sm:ml-6 sm:flex sm:space-x-4">
                <NavLink to="/" className={navLinkClass} end>
                  Overview
                </NavLink>
                <NavLink to="/clusters" className={navLinkClass}>
                  Clusters
                </NavLink>
                <NavLink to="/system" className={navLinkClass}>
                  System
                </NavLink>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Page content goes here */}
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout; 