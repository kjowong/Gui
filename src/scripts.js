import React from 'react';
import ReactDOM from 'react-dom';

// Creates the main div component
class Main extends React.Component {
  constructor () {
 	super();
    this.state = {
      priceQuery: '',
      searchQuery: '',
      results: []
    };
    this.handlePrice = this.handlePrice.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  // Function to handle the click
  handleClick () {
    let url;

    // Endpoint changes depending on if price was selected
    if (this.state.priceQuery === '') {
    	url = `http://0.0.0.0:5000/search/${this.state.searchQuery}`;
    } else {
    	url = `http://0.0.0.0:5000/search/${this.state.searchQuery}/${this.state.priceQuery}`;
    }

    // Using axios to make api call
    axios.get(url).then(response => {
      // Store response into an array of objects
      const restaurants = response.data.map(place => place);
      console.log('REST', restaurants);
      console.log('----------');
      // Set the state when response is returned
      this.setState({
		    results: restaurants
	        });
    });
  }

  // Function to handle keypress - not implemented yet
  handleKeyPress (event) {
    if (event.charCode == 13) {
      event.preventDefault();
      this.props.handleClick();
    }
  }

  // Function to handle the price coming in
  handlePrice (e) {
    // Sets the state to the price user selected
    this.setState({
      priceQuery: e.target.value
    });
  }

  // Function to handle the change when user inputs new zip
  handleChange (e) {
    // Sets the state to the zip user typed
    this.setState({
      searchQuery: e.target.value
    });
  }

  // Render the main div
  render () {
    // If the results if empty, do not mount results component
    if (this.state.results.length === 0) {
      return (
        <div className='parent-div'>
          <header className='masthead'>
            <div className='price-search-results'>
              <Price
                priceQuery={this.state.priceQuery}
                handlePrice={this.handlePrice} />
              <Search
                searchQuery={this.state.searchQuery}
                handleChange={this.handleChange}
                handleClick={this.handleClick} />
            </div>
          </header>
        </div>
      );
    } else { // If results is not empty, mount the results component
      return (
        <div className='parent-div'>
          <header className='masthead'>
            <div className='price-search-results'>
              <Price
                priceQuery={this.state.priceQuery}
                handlePrice={this.handlePrice} />
              <Search
                searchQuery={this.state.searchQuery}
                handleChange={this.handleChange}
                handleClick={this.handleClick} />
            </div>
          </header>
          <Results results={this.state.results} />
        </div>
      );
    }
  }
 }

// Component to handle scroll
class ScrollButton extends React.Component {
  constructor () {
    super();
    // Initial state of 0
    this.state = {
      intervalId: 0
    };
  }
  // Function to reset scroll if at the top
  scrollStep () {
    if (window.pageYOffset === 0) {
      clearInterval(this.state.intervalId);
    }
    window.scroll(0, window.pageYOffset - this.props.scrollStepInPx);
  }
  // Function to scroll to top of page
  scrollToTop () {
    let intervalId = setInterval(this.scrollStep.bind(this), this.props.delayInMs);
    this.setState({ intervalId: intervalId });
  }
  // Renders the scroll component
  render () {
    return <button title='Back to top' className='scroll'
      onClick={() => { this.scrollToTop(); }} />;
  }
}

// Search component to handle search div
class Search extends React.Component {
  render () {
    return (
      <div className='search'>
        <div className='search-send'>
          <input
            className='search-input'
            placeholder='Zip code'
            type='search'
            value={this.props.searchQuery} // inverser dataflow
            onChange={this.props.handleChange} />
          <button className='search-button' onClick={this.props.handleClick}><i className='fa fa-search' /></button>
        </div>
      </div>
    );
  }
}
// Price component to handle the price div
class Price extends React.Component {
  render () {
    console.log('PriceQuery', this.props.priceQuery);
    return (
      <div className='price-div'>
        <select
          className='dropdown'
          value={this.props.priceQuery}
          onChange={this.props.handlePrice}>
          <option value=''>All</option>
          <option value='1'>$</option>
          <option value='2'>$$</option>
          <option value='3'>$$$</option>
          <option value='4'>$$$$</option>
        </select>
      </div>
    );
  }
}

// Results component to handle the results div
class Results extends React.Component {
  // If the results was able to mount, scroll to the results div
  componentDidMount () {
    ReactDOM.findDOMNode(this).scrollIntoView();
  }
  // If the results was updated, scroll to the results div
  componentDidUpdate () {
    ReactDOM.findDOMNode(this).scrollIntoView();
  }
  // Render the results
  render () {
     // Function to sort the results to the highest composite to lowest score
    this.props.results.sort(function (firstComposite, secondComposite) {
      return secondComposite.composite - firstComposite.composite;
    });
    // Grabs the tips dict and store in a variable
    let tipsDict;
    for (let i = 0; i < this.props.results.length; i++) {
      if (this.props.results[i]['tips_dict']) {
    	 tipsDict = this.props.results[i]['tips_dict'];
      }
    }
    // Return the results div
    // Maps each item in results and calls the ResultsItem component to create the list
    return (
      <div className='results-info'>
        <div className='results-pop-info'>
	    The <strong>{tipsDict['subzone']}</strong> district has a foodie rating of <strong>{tipsDict['popularity']}</strong> and a nightlife rating of <strong>{tipsDict['nightlife_index']}</strong>. The most popular restaurant categories in this area are: <span />
          {
	    	tipsDict['top_cuisines'].map((item, i) => <span key={i}>{item}</span>).map((item, index) => [index > 0 && ', ', item ])
	  }
        </div>
        <div className='results'>
          {
		this.props.results.filter(i => !i.tips_dict).map((item, i) => <ResultItem item={item} key={i} />)
 	  }
          <ScrollButton scrollStepInPx='50' delayInMs='16.66' />
        </div>
      </div>
    );
  }
}

// ResultItem Component, handles each list item for each result item
class ResultItem extends React.Component {
  render () {
    // If there is no image, use a default image
    let source = this.props.item['image_url'];
    if (!source) {
      source = 'https://i.imgur.com/HgxNiNM.png';
    }
    // Return the result list
    return (
      <article className='one-restaurant'>
        <ul className='restaurant-list'>
          <h3>{this.props.item['name']}</h3>
          <div className='image-restaurant'>
            <img className='image-place' src={source} />
            <div className='tips'>
              <p><i>"{this.props.item['tip']}"</i></p>
            </div>
            <div className='guiscore'>
              <p>Gui Score: {this.props.item['composite']}</p>
            </div>
          </div>
          <p />
          <div className='out-progress-bar w3-round-xlarge'>
            <div
              className='w3-green w3-round-xlarge'
              style={{width: this.props.item['composite'] + '%'}}>
              {this.props.item['composite']}</div>
          </div>
          <p className='list-padding' />
          <li>{this.props.item['location']}</li>
          <li>{this.props.item['phone_num']}</li>
          <li>Total Reviews:
	    <strong> {this.props.item['total_reviews']}</strong>
          </li>
          <p>---------------------------------------</p>
          <li>Price Tier: {this.props.item['price_range']}</li>
        </ul>
      </article>
    );
  }
}
// Render the main div with id root
ReactDOM.render(<Main />, document.getElementById('root'));
