const clamp = (min, max) => (value) => value < min ? min : value > max ? max : value;

class ScrollbarThumb {
    /**
     * @param {HTMLElement} thumb 
     * @param {HTMLElement} scrollTarget
     */
    constructor(thumb, scrollTarget) {
        this.thumb = thumb;
        this.target = scrollTarget;

        this.thumb.ondragstart = () => false;
        this.thumb.parentElement.ondragstart = () => false;

        const isVertical = this.thumb.parentElement.classList.contains("scrollbar-vertical");

        this.thumb.onmousedown = (_event) => {            
            const trackRect = this.thumb.parentElement.getBoundingClientRect();
            const thumbRect = this.thumb.getBoundingClientRect();
            
            const onmousemove = (isVertical ? this.getMousemoveVertical : this.getMousemoveHorizontal)
                .call(this, _event, trackRect, thumbRect);

            const onmouseup = (event) => {
                if (event.which == 1) {
                    window.removeEventListener('mousemove', onmousemove);
                    window.removeEventListener('mouseup', onmouseup);
                }
            }
            
            window.addEventListener('mousemove', onmousemove);
            window.addEventListener("mouseup", onmouseup);
        }
    }

    getMousemoveVertical(_event, trackRect, thumbRect) {
        const trackLength = trackRect.height - thumbRect.height;
        const scrollbarClamp = clamp(0, trackLength);
        const shiftY = _event.pageY - thumbRect.y;
        return (event) => {
            const y = scrollbarClamp(event.pageY - trackRect.y - shiftY);
            this.thumb.style.transform = `translateY(${y}px)`;
            this.target.scroll(0, (y / trackLength) * (this.target.scrollHeight - this.target.clientHeight));
        };
    }

    getMousemoveHorizontal(_event, trackRect, thumbRect) {
        const trackLength = trackRect.width - thumbRect.width;
        const scrollbarClamp = clamp(0, trackLength);
        const shiftX = _event.pageX - thumbRect.x;
        return (event) => {
            const x = scrollbarClamp(event.pageX - trackRect.x - shiftX);
            this.thumb.style.transform = `translateX(${x}px)`;
            this.target.scroll((x / trackLength) * (this.target.scrollWidth - this.target.clientWidth), 0);
        };
    }
}