(function() {
	HTMLElement.prototype.tap = function(fn, e_d, t_i) {
		var func = function(e) {
			e = e || window.event;
			var callee = arguments.callee;
			var now = new Date().getTime();
			var event_type = e.type.toLocaleLowerCase().replace("on", "");
			//check event type
			if((event_type=="click")&&(now - callee.last_execute > callee.execute_delay)) {
				callee.last_call = now;
				callee.last_execute = now;
				callee.last_event = "click";
				fn.call(this);
			} else if(event_type=="touchstart") {
				callee.last_call = now;
				callee.last_event = "touchstart";
			} else if((event_type=="touchend")&&(callee.last_event=="touchstart")&&(now - callee.last_call < callee.tap_interval)&&(now - callee.last_execute > callee.execute_delay)) {
				callee.last_call = now;
				callee.last_execute = now;
				callee.last_event = "touchend";
				fn.call(this);
			} else if(event_type=="touchmove") {
				callee.last_call = now;
				callee.last_event = "touchmove";
			}
		};
		//set last call and last execute variables
		func.last_call = new Date().getTime();
		func.last_execute = new Date(1970, 1, 1);
		func.last_event = null;
		//standard execute delay
		func.execute_delay = e_d || 60;
		func.tap_interval = t_i || 60;
		//attach event handlers
		if(this.addEventListener) {
			this.addEventListener("click", func);
			this.addEventListener("touchstart", func);
			this.addEventListener("touchend", func);
			this.addEventListener("touchmove", func);
		} else {
			this.attachEvent("onclick", func);
			this.attachEvent("ontouchstart", func);
			this.attachEvent("ontouchend", func);
			this.attachEvent("ontouchmove", func);
		}
	};
})();
