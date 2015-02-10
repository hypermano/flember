import Ember from 'ember';

export default Ember.Route.extend({
	model: function() {
		return this.store.createRecord('snippet');
	},
	actions: {
		willTransition: function(){
			this.controller.get('model').rollback();
		}
	}
});
