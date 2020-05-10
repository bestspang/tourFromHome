/* --------------------------------
 * Simple login, registration and
 * recover password form swap with
 * a basic ripple effect and a
 * simple floating label example.
 *
 * @version 1.0
 * -------------------------------- */
$(document).ready(function(){

(function () {
	'use strict';

	/**
	 * CLASSES
	 * ------- */

	var CLASSES = {
		button		: 'btn',
		checkbox	: 'toggle__checkbox',
		container	: 'mainContainer',
		form			: '[data-toggle="form"]',
		input			: 'inputfield__input',
		inputfield: 'inputfield'
	};

	/**
	 * TOGGLE CLASSES
	 * -------------- */

	var IS_ACTIVE			= 'is-active';
	var IS_ANIMATING	= 'is-animating';
	var IS_DIRTY			= 'is-dirty';

	var CONTAINER_CLASSES = [
		'is-amnesia', 'is-login', 'is-register'
	];

	/**
	 * ELEMENTS
	 * -------- */

	var BUTTON			= document.querySelectorAll('.' + CLASSES.button);
	var CHECKBOX		= document.querySelectorAll('.' + CLASSES.checkbox);
	var CONTAINER		= document.getElementById(CLASSES.container);
	var FORMTOGGLE	= document.querySelectorAll(CLASSES.form);
	var INPUTFIELD	= document.querySelectorAll('.' + CLASSES.inputfield);

	/**
	 * Animation end event.
	 * @link https://davidwalsh.name/css-animation-callback
	 * @return	mixed
	 */
	var whichAnimationEvent = function () {
		var a;
		var el = document.createElement('loginfakeelement');
		var animations = {
			'animation'				:'animationend',
			'OAnimation'			:'oAnimationEnd',
			'MozAnimation'		:'animationend',
			'WebkitAnimation'	:'webkitAnimationEnd'
		};

		for (a in animations) {
			if (el.style[a] !== undefined) {
				return animations[a];
			}
		}

		return false;
	};

	/**
	 * Check if device is mobile.
	 * @link https://tympanus.net/codrops/?p=23217
	 * @return	boolean
	 */
	var mobileCheck = function () {
		var check = false;

		(function (a) {
			if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(a)) {
				check = true;
			}
		})(navigator.userAgent || navigator.vendor || window.opera);

		return check;
	};

	// Get event type.
	var eventType = mobileCheck() ? 'touchstart' : 'click';
	var eventBtn	= mobileCheck() ? 'touchstart' : 'mousedown';

	// Animation end short var.
	var animationEnd = whichAnimationEvent();

	/**
		* Toggle animation class.
		* @return	void
		*/
	var animationClassToggle = function () {
		// Add `animating` class.
		this.classList.add(IS_ANIMATING);

		// Remove `animating` class if
		// animations are not supported.
		if ( ! animationEnd) {
			this.classList.remove(IS_ANIMATING);

			return;
		}

		// Remove `animating` class on animation end.
		animationEnd && this.addEventListener(animationEnd, function () {
			if (this.classList.contains(IS_ANIMATING)) {
				this.classList.remove(IS_ANIMATING);
			}
		});
	};

	/**
	 * Checkbox ripple event.
	 * @see checkBoxRipple	LESS/CSS
	 * @see animationClassToggle()
	 */
	[].slice.call(CHECKBOX).forEach(function (el) {
		el.addEventListener(eventBtn, animationClassToggle.bind(el));
	});

	/**
	 * Button ripple event.
	 * @see btnRipple		LESS/CSS
	 * @see animationClassToggle()
	 */
	[].slice.call(BUTTON).forEach(function (el) {
		el.addEventListener(eventBtn, animationClassToggle.bind(el));
	});

	/**
	 * Toggle forms.
	 */
	[].slice.call(FORMTOGGLE).forEach(function (el) {
		var $target = document.getElementById(el.getAttribute('data-target'));
		var $type = 'is-' + el.getAttribute('data-type');

		// Add `touchstart` or `click` event.
		el.addEventListener(eventType, function (e) {
			if (e) e.preventDefault();

			// If a target doesn't exist, simply do nothing.
			if ( ! $target) return;

			// Find all children of target parent element.
			var children = $target.parentNode.children;

			// Remove `active` class from target siblings.
			Array.prototype.filter.call(children, function (child) {
				if (child !== $target) {
					child.classList.remove(IS_ACTIVE);
				}
			});

			// Add `active` class to target form.
			if ( ! $target.classList.contains(IS_ACTIVE)) {
				$target.classList.add(IS_ACTIVE);
			}

			// Remove current active container class.
			CONTAINER_CLASSES.forEach(function (c) {
				CONTAINER.classList.remove(c);
			});

			// Add new active container class.
			CONTAINER.classList.add($type);
		});
	});

	/**
	 * Inputfields.
	 */
	[].slice.call(INPUTFIELD).forEach(function (el) {
		var input = el.querySelector('.' + CLASSES.input);
		/**
		 * Check input value and add/remove
		 * class accordingly.
		 * @return	void
		 */
		var checkValue = function () {
			if (input.value != '' && ! el.classList.contains(IS_DIRTY)) {
				el.classList.add(IS_DIRTY);
			} else if (input.value == '' && el.classList.contains(IS_DIRTY)) {
				el.classList.remove(IS_DIRTY);
			}
		};

		// Add `input` and `change` event listeners.
		input.addEventListener('input', checkValue);
		input.addEventListener('change', checkValue);

		// Check value on content load.
		document.addEventListener('DOMContentLoaded', checkValue);
	});

})();

//add

});
