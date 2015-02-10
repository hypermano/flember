import Ember from 'ember';

export default Ember.Route.extend({
	model: function() {
		return this.store.find('snippet');
	},
	actions: {
		saveSnippet: function(snippet) {
			snippet.save().then(function() {
				this.transitionTo('snippets.index');
			}.bind(this));
		},
		deleteSnippet: function(snippet) {
			snippet.destroyRecord().then(function() {
				this.transitionTo('snippets.index');
			}.bind(this));
		}
	}

});
