var LazyImage = {
	Parse:function() {
		var els = document.querySelectorAll("[data-lazy]");
		for(var i = 0; i < els.length; i++) {
			var el  = els[i];
			el._index = -1;
			var imgs = el.getAttribute("data-lazy").split(";");
			el.removeAttribute("data-lazy");
			for(var j = 0; j < imgs.length; j++) {
				var img = new Image();
				img.onload = function() {
					if(this._index > this._reference._index) {
						if(this._reference.tagName.toUpperCase()=="IMG") {
							this._reference.src = this.src;
						} else { this._reference.style.backgroundImage = "url("+this.src+")"; }
						this._reference._index = this._index;
					}
				}
				img._index = j;
				img._reference = el;
				img.src = imgs[j];
			}
		}
	}
};
LazyImage.Parse();
