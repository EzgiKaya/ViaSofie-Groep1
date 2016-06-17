HTMLElement.prototype.hasClass = function(className) {
    var classes = this.className.split(' ');
    if(classes.indexOf(className) > -1)
        return true;
    else return false;
}
HTMLElement.prototype.addClass = function(className) {
    if(!this.hasClass(className)) {
        if(this.className.trim().length>0) { this.className += ' '; }
        this.className += className;
    }
}
HTMLElement.prototype.removeClass = function(className) {
    var classes = this.className.split(' ');
    var idx = classes.indexOf(className);
    if(idx > -1) {
        var newClass = '';
        classes.splice(idx, 1);
        for(var i = 0; i < classes.length; i++) {
            if(classes[i].trim()!='') {
                if(i>0) { newClass+=' '; }
                newClass+=classes[i];
            }
        }
        this.className = newClass;
    }
}
