import pandas as pd

data = {
    'Room': ['A101', 'A102', 'B201', 'B202', 'C301'],
    'Building': ['A', 'A', 'B', 'B', 'C'],
    'capacity': [30, 25, 50, 40, 60],
    'amenities': ['["Projector", "Whiteboard"]', '["Whiteboard"]', '["Projector", "Podium"]', '["Projector"]', '["Projector", "Whiteboard", "Podium"]'],
    'photo_url': [
        'https://images.unsplash.com/photo-1567589008473-76c02936a352?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'https://images.unsplash.com/photo-1590479600959-a3e27943c433?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'https://images.unsplash.com/photo-1563245929-176bf0575475?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    ]
}

df = pd.DataFrame(data)
df.to_excel("D:\\engineering\\experiments\\siara\\roomfinder\\sample_data\\rooms.xlsx", index=False)
