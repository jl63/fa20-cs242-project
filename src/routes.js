import React from 'react';
import { Route, IndexRoute } from 'react-router';

/**
 * Import all page components here
 */
import App from './components/App';
import HomePage from './components/HomePage';
import SearchResultPage from './components/SearchResultPage';

/**
 * All routes go here.
 * Don't forget to import the components above after adding new route.
 */
export default (
    <Route path="/" component={App}>
        <IndexRoute component={HomePage} />
        <Route path="/search/result" component={SearhResultPage} />
    </Route>
);