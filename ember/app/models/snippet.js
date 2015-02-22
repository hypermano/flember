import DS from 'ember-data';

export default DS.Model.extend({
  text: DS.attr('string', {
  	defaultValue: 'Nothing'
  }),
  date: DS.attr('string'),
  textChanged: function() {
  	if (this.get("isDirty") && !this.get("isNew")) {
  		// this.save();
  	}
  }.observes('text')
});
