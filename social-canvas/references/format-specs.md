# Social Media Format Specifications

## Dimensions Reference

| Format | Width | Height | Aspect | Safe Zone | Max Slides | Notes |
|--------|-------|--------|--------|-----------|------------|-------|
| LinkedIn Carousel | 1080 | 1080 | 1:1 | 60px all sides | 10 | Square default. Use 1080x1350 (4:5) only when content needs more vertical space. PDF upload also supported. |
| Instagram Carousel | 1080 | 1080 | 1:1 | 60px all sides | 10 | Square format, mobile-first |
| Instagram Story | 1080 | 1920 | 9:16 | 60px sides, 120px top/bottom | 1 | Top/bottom UI overlay zones |
| Twitter/X Post | 1200 | 675 | 16:9 | 40px all sides | 1 | Landscape, less vertical space |
| Single Infographic | 1080 | 1350 | 4:5 | 60px all sides | 1 | Vertical, shareable |

## Safe Zones

Safe zones account for:
- Platform UI overlays (profile pics, like buttons, swipe indicators)
- Corner rounding on some platforms
- Thumbnail cropping in feeds

**Rule**: No critical text or visual elements within the safe zone boundary. Decorative elements (background patterns, gradients) may extend to edges.

## Typography Scale (minimum sizes for legibility on mobile)

| Element | Min Size | Recommended | Max Size |
|---------|----------|-------------|----------|
| Headline | 48px | 64-80px | 120px |
| Subhead | 32px | 36-48px | 56px |
| Body | 24px | 28-32px | 36px |
| Caption/Label | 18px | 20-24px | 28px |
| Large Number (stat) | 80px | 120-160px | 200px |

## Rendering Settings

- `device_scale_factor`: 1 (exact pixel output, no Retina scaling)
- Font loading wait: 800ms after networkidle
- Screenshot: viewport-clipped (not full-page)
