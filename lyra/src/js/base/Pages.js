import React from 'react';
import { useRoutes } from 'hookrouter';
import Home from './pages/Home';

const routes = {
  '/': () => <Home />
};

const Pages = () => {
  return useRoutes(routes);
}

export default Pages;