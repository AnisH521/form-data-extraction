import cv2
import numpy as np

def get_optimal_display_size(img_shape, max_width=1200, max_height=800):
    """Calculate optimal size to fit image on screen while maintaining aspect ratio."""
    h, w = img_shape[:2]
    
    # Calculate scaling factor
    scale_w = max_width / w
    scale_h = max_height / h
    scale = min(scale_w, scale_h, 1.0) 
    
    new_width = int(w * scale)
    new_height = int(h * scale)
    
    return new_width, new_height, scale

def click_event(event, x, y, flags, params):
    global img_display, img_original, scale_factor
    
    # Convert display coordinates to original image coordinates
    orig_x = int(x / scale_factor)
    orig_y = int(y / scale_factor)
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Display coordinates: ({x}, {y})")
        print(f"Original image coordinates: ({orig_x}, {orig_y})")
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Draw on display image
        cv2.circle(img_display, (x, y), 5, (0, 255, 0), -1)
        text = f"({orig_x},{orig_y})"
        cv2.putText(img_display, text, (x+10, y-10), font, 0.6, (255, 0, 0), 2)
        cv2.imshow('image', img_display)

    if event == cv2.EVENT_RBUTTONDOWN:
        # Get BGR from original image
        if 0 <= orig_y < img_original.shape[0] and 0 <= orig_x < img_original.shape[1]:
            b, g, r = img_original[orig_y, orig_x]
            print(f"Original BGR at ({orig_x}, {orig_y}): ({b}, {g}, {r})")
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"BGR:({b},{g},{r})"
            cv2.putText(img_display, text, (x+10, y+20), font, 0.5, (255, 255, 0), 2)
            cv2.imshow('image', img_display)

if __name__ == "__main__":
    # Load original image
    img_original = cv2.imread(r'data/form_4.jpeg', 1)
    
    if img_original is None:
        print("Error: Could not load image. Check the file path.")
        exit()
    
    print(f"Original image size: {img_original.shape[1]} x {img_original.shape[0]}")
    
    # Calculate optimal display size
    display_width, display_height, scale_factor = get_optimal_display_size(img_original.shape)
    print(f"Display size: {display_width} x {display_height}, Scale: {scale_factor:.3f}")
    
    img_display = cv2.resize(img_original, (display_width, display_height), interpolation=cv2.INTER_AREA)
    
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('image', img_display)
    cv2.setMouseCallback('image', click_event)
    
    print("Instructions:")
    print("- Left click: Show coordinates (both display and original)")
    print("- Right click: Show BGR values from original image")
    print("- Press 'q' to quit")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
