G='#4F7230'; R='#B03024'; B='#52372A'
NO=f'<circle cx="12" cy="12" r="10" stroke="{R}"/><path d="M5 5l14 14" stroke="{R}"/>'
I=[
# 1 gear: glove + boot
'<path d="M6 20v-5l-2.2-3a1.1 1.1 0 0 1 1.8-1.3L7 12.5V5.6a1 1 0 0 1 2 0V11M9 11V4.4a1 1 0 0 1 2 0V11M11 11V5a1 1 0 0 1 2 0v6M13 11.5V7a1 1 0 0 1 2 0v7c0 3-1.4 6-4.4 6H6"/><path d="M6 17.5h7"/>'
 f'<path d="M17 9h3v8l2.5 1.2V21H16v-4z" stroke="{B}"/>',
# 2 check edges: bin + magnifier
'<path d="M1.5 12.5h12l-1.5 8H3z" stroke="#52372A"/><path d="M2.5 10.5l1-1.8 1 1.8M6 10.5l1-1.8 1 1.8" stroke="#B03024"/><circle cx="17" cy="8" r="4"/><path d="M20 11l2.5 2.5"/>',
# 3 kids & pets
'<circle cx="7" cy="5" r="2"/><path d="M7 7v6M4 10h6M7 13l-2 6M7 13l2 6"/>'
 f'<g stroke="{B}"><circle cx="15" cy="13" r="1.1"/><circle cx="18" cy="11.8" r="1.1"/><circle cx="21" cy="13" r="1.1"/><path d="M15.6 18.5c0-2 1.2-3.2 2.4-3.2s2.4 1.2 2.4 3.2c0 1-.8 1.5-2.4 1.5s-2.4-.5-2.4-1.5z"/></g>',
# 4 clear path
'<path d="M5 21c1-4 3-5 7-6s6-3 5-7-3-5-5-6" stroke-dasharray="2.2 2.4"/><path d="M3 21h4M15 2h4"/>',
# 5 weather: sun + cloud + snowflake
'<circle cx="8" cy="8" r="3"/><path d="M8 2v1.5M8 12.5V14M2 8h1.5M12.5 8H14M3.8 3.8l1 1M11.2 11.2l1 1M3.8 12.2l1-1M11.2 4.8l1-1"/>'
 f'<path d="M11 21h7.5a3 3 0 0 0 0-6 4.2 4.2 0 0 0-8 1.2A2.4 2.4 0 0 0 11 21z" stroke="{B}"/>',
# 6 sort: big and small boxes
'<rect x="2.5" y="11" width="9" height="9" rx="1"/><path d="M2.5 14h9M7 11v3"/><rect x="14" y="14" width="6" height="6" rx="1"/><path d="M14 4h7M18 1.5L21 4l-3 2.5" stroke="#52372A"/>',
# 7 can't go in: battery + no
'<rect x="7" y="8.5" width="9" height="7" rx="1" stroke="#52372A"/><path d="M16 11v2" stroke="#52372A"/>'+NO,
# 8 test weight: kettlebell kg
'<path d="M9 10V8a3 3 0 0 1 6 0v2"/><path d="M6.5 10h11l2 10h-15z"/><text x="12" y="18" font-size="5.5" text-anchor="middle" fill="#4F7230" stroke="none" font-family="Arial,sans-serif" font-weight="700">kg</text>',
# 9 lifting posture: squat, straight back, box
'<circle cx="8" cy="4" r="2"/><path d="M8 6l1 6h5M9 12l-2 3 1 5M14 12l-1 3 1 5"/><path d="M9 8.5l5 1.5"/><rect x="14" y="7" width="7" height="6" rx="0.8" stroke="#52372A"/>',
# 10 keep the load close: hug box
'<circle cx="12" cy="4" r="2"/><path d="M12 6v8M10.5 14l-1 6M13.5 14l1 6"/><rect x="8.5" y="8" width="7" height="5" rx="0.8" stroke="#52372A"/><path d="M8 9.5h-1v2.5h1.5M16 9.5h1v2.5h-1.5"/>',
# 11 don't twist
'<path d="M16.5 6.5A7 7 0 1 0 19 12"/><path d="M16 2.5v4h4"/><path d="M9.5 9.5l5 5M14.5 9.5l-5 5" stroke="#B03024"/>',
# 12 two people lifting
'<circle cx="5" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><path d="M5 7v7M19 7v7M5 14l-1.5 6M5 14l1.5 6M19 14l-1.5 6M19 14l1.5 6M5 10h3M19 10h-3"/><rect x="8" y="8" width="8" height="5" rx="0.8" stroke="#52372A"/>',
# 13 wheelbarrow
'<path d="M2 8h14l-3 6H6z"/><circle cx="17" cy="17" r="2.6"/><path d="M13 14l4 3M6 14l-2 6M2 8L1 6"/>',
# 14 pace: cup + steam
'<path d="M5 10h11v4a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5z"/><path d="M16 11h1.5a2.5 2.5 0 0 1 0 5H16"/><path d="M8.5 3c0 1.5 1.5 1.5 1.5 3M12.5 3c0 1.5 1.5 1.5 1.5 3" stroke="#52372A"/><path d="M4 22h14"/>',
# 15 heavy first: bricks + down arrow
'<rect x="2.5" y="15" width="9" height="5" rx="0.6"/><rect x="12.5" y="15" width="9" height="5" rx="0.6"/><rect x="7.5" y="9.5" width="9" height="5" rx="0.6"/><path d="M12 1.5V7M9.5 4.8L12 7.2l2.5-2.4" stroke="#52372A"/>',
# 16 break it down: handsaw
'<path d="M3 19L15 7l3 3L6 22z"/><path d="M5 20.5l-.8-.8M7 18.5l-.8-.8M9 16.5l-.8-.8M11 14.5l-.8-.8M13 12.5l-.8-.8"/><path d="M15 7l2.5-2.5a1.5 1.5 0 0 1 2 0l2 2a1.5 1.5 0 0 1 0 2L19 11" stroke="#52372A"/>',
# 17 load level: bin + spirit level
'<path d="M3 11h18l-2.2 9.5H5.2z"/><rect x="2" y="6" width="20" height="3.2" rx="1" stroke="#52372A"/><rect x="10" y="6.6" width="4" height="2" rx="1" stroke="#52372A"/>',
# 18 heavy waste: scales
'<path d="M12 3v16M7 21h10M4 6h16"/><path d="M4 6l-2.5 6h5zM20 6l-2.5 6h5z"/><path d="M1.5 12a2.5 2 0 0 0 5 0M17.5 12a2.5 2 0 0 0 5 0"/>',
# 19 sharps: nail + shard
'<path d="M5 4h8M9 4v11"/><path d="M8 15h2l-1 5z"/><path d="M15 21l3-9 4 6z" stroke="#B03024"/>',
# 20 don't climb in
'<path d="M7 18l1.2-6h7.6l1.2 6z" stroke="#52372A"/><circle cx="12" cy="6" r="1.6"/><path d="M12 7.6v3M12 9l-2.2 1.4M12 9l2 1M12 10.6l-1.5 2.4" />'+NO,
# 21 don't throw in
'<path d="M7 19l1-5h8l1 5z" stroke="#52372A"/><path d="M12 4v7M9.5 8.5L12 11l2.5-2.5"/>'+NO,
# 22 cover if rain
'<path d="M6 13h11a3.5 3.5 0 0 0 0-7 5 5 0 0 0-9.6 1.4A2.9 2.9 0 0 0 6 13z"/><path d="M7 16l-1 2M11 16l-1 2M15 16l-1 2M9 19.5l-.8 1.5M13 19.5l-.8 1.5" stroke="#52372A"/>',
# 23 truck access
'<rect x="1.5" y="7" width="12" height="9" rx="1"/><path d="M13.5 10h4l3 3v3h-7"/><circle cx="6" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>',
# 24 keep clear: stop hand
'<path d="M8 13V6a1.2 1.2 0 0 1 2.4 0v5M10.4 11V4.2a1.2 1.2 0 0 1 2.4 0V11M12.8 11V5a1.2 1.2 0 0 1 2.4 0v6M15.2 11.5V7.5a1.2 1.2 0 0 1 2.4 0V15c0 3.5-2.2 6-5.6 6-2.6 0-3.8-1.5-4.8-3.4L5.3 14a1.3 1.3 0 0 1 2.1-1.4L8 13.5"/>',
# 25 phone
'<path d="M6 3h3.5l1.8 4.6-2.3 1.4a11 11 0 0 0 5.9 5.9l1.4-2.3L21 14.5V18a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 2-2z"/>',
]
def svg(i): return ('<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'%(G,I[i]))
