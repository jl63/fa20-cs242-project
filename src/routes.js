import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";

import history from './histroy';

/**
 * Import all page components here
 */
import HomePage from './components/HomePage';
import SearchResultPage from './components/SearchResultPage';

/**
 * All routes go here.
 * Don't forget to import the components above after adding new route.
 */
export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact component={HomePage} />
                    <Route path = "/searchResults" component={SearchResultPage}/>
                </Switch>
            </Router>
        )
    }
}