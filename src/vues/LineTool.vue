<script>
// Line drawing tool
// TODO: make an angle-snap when "Shift" is pressed

import { Overlay } from '../../../trading-vue-js'
import { Tool } from '../../../trading-vue-js'
import Icons from '../../data/icons.json'
import { Pin } from '../../../trading-vue-js'
import { Seg } from '../../../trading-vue-js'
import { Line } from '../../../trading-vue-js'
import { Ray } from '../../../trading-vue-js'

export default {
    name: 'LineTool',
    mixins: [Overlay, Tool],
    methods: {
        meta_info() {
            return { author: 'C451', version: '1.1.0' }
        },
        tool() {
            return {
                // Descriptor for the tool
                group: 'Lines1', icon: Icons['buy_sell.png'],
                type: 'Segment',
                hint: 'This hint will be shown on hover',
                data: [],     // Default data
                settings: {}, // Default settings
                // Modifications
                mods: {
                    'Extended': {
                        // Rewrites the default setting fields
                        settings: { extended: true },
                        icon: Icons['extended.png']
                    },
                    'Ray': {
                        // Rewrites the default setting fields
                        settings: { ray: true },
                        icon: Icons['ray.png']
                    }
                }
            }
        },
        // Called after overlay mounted
        init() {
            // First pin is settled at the mouse position
            this.pins.push(new Pin(this, 'p1'))
            // Second one is following mouse until it clicks
            this.pins.push(new Pin(this, 'p2', {
                state: 'tracking'
            }))
            this.pins[1].on('settled', () => {
                // Call when current tool drawing is finished
                // (Optionally) reset the mode back to 'Cursor'
                this.set_state('finished')
                this.$emit('drawing-mode-off')
            })
        },
        draw(ctx) {
            if (!this.p1 || !this.p2) return

            ctx.lineWidth = this.line_width
            ctx.strokeStyle = this.color
            ctx.beginPath()

            if (this.sett.ray) {
                new Ray(this, ctx).draw(this.p1, this.p2)
            } else if (this.sett.extended) {
                new Line(this, ctx).draw(this.p1, this.p2)
            } else {
                new Seg(this, ctx).draw(this.p1, this.p2)
            }

            ctx.stroke()
            this.render_pins(ctx)

        },
        use_for() { return ['LineTool1'] },
        data_colors() { return [this.color] }
    },
    // Define internal setting & constants here
    computed: {
        sett() {
            return this.$props.settings
        },
        p1() {
            return this.$props.settings.p1
        },
        p2() {
            return this.$props.settings.p2
        },
        line_width() {
            return this.sett.lineWidth || 0.9
        },
        color() {
            return this.sett.color || '#42b28a'
        }
    },
    data() {
        return {}
    }

}
</script>