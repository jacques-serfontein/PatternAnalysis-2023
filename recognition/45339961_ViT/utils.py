""" Utility functions for generic use. """

import matplotlib.pyplot as plt
from torch.utils.data import DataLoader

def plot_losses_accuracies(train_accuracies,
            valid_accuracies,
            train_losses,
            valid_losses):
    labels = ['Train', 'Valid']

    # Create x-axis values (epochs)
    epochs = range(1, len(train_accuracies) + 1, 1)

    # Create a 1x2 grid of subplots
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Plot accuracy data on the first subplot
    axs[0].plot(epochs, train_accuracies, label=labels[0])
    axs[0].plot(epochs, valid_accuracies, label=labels[1])
    axs[0].set_title('Accuracy Over Epochs')
    axs[0].set_xlabel('Epoch')
    axs[0].set_ylabel('Accuracy')
    axs[0].legend(loc='best')
    axs[0].grid(True)

    # Plot loss data on the second subplot
    axs[1].plot(epochs, train_losses, label=labels[0])
    axs[1].plot(epochs, valid_losses, label=labels[1])
    axs[1].set_title('Loss Over Epochs')
    axs[1].set_xlabel('Epoch')
    axs[1].set_ylabel('Loss')
    axs[1].legend(loc='best')
    axs[1].grid(True)

    # Adjust spacing between plots
    plt.tight_layout()

    # Show the plots
    plt.show()

# Function uses a modification of the code found in 
# https://www.learnpytorch.io/08_pytorch_paper_replicating/#44-flattening-the-patch-embedding-with-torchnnflatten
def show_patched_image(img, img_size, patch_size):
    """ Plot a permuted image as a series of patches. """
    # Setup hyperparameters and make sure img_size and patch_size are compatible
    num_patches = img_size/patch_size

    # Create a series of subplots
    fig, axs = plt.subplots(nrows=img_size // patch_size, # need int not float
                            ncols=img_size // patch_size, 
                            figsize=(num_patches, num_patches),
                            sharex=True,
                            sharey=True)
    
    # Set the spacing between subplots
    fig.subplots_adjust(wspace=0.1, hspace=0.1)

    # Loop through height and width of image
    for i, patch_height in enumerate(range(0, img_size, patch_size)): # iterate through height
        for j, patch_width in enumerate(range(0, img_size, patch_size)): # iterate through width
            
            # Plot the image patch
            axs[i, j].imshow(img[patch_height:patch_height+patch_size,  # iterate through height 
                                            patch_width:patch_width+patch_size], # iterate through width
                                            cmap = "gray") 
            
            # Set up label information, remove the ticks for clarity and set labels to outside
            axs[i, j].set_ylabel(i+1, 
                                rotation="horizontal", 
                                horizontalalignment="right", 
                                verticalalignment="center") 
            axs[i, j].set_xlabel(j+1) 
            axs[i, j].set_xticks([])
            axs[i, j].set_yticks([])
            axs[i, j].label_outer()

    # Set a super title
    fig.suptitle("Example patched image", fontsize=16)
    plt.show()

# This function was based on the solution provided in:
# https://discuss.pytorch.org/t/computing-the-mean-and-std-of-dataset/34949/2
def determine_mean_std_dataset(dataset):
    """ Determine the mean and standard deviation of a dataset. """
    loader = DataLoader(dataset,
                        batch_size=64,
                        num_workers=4,
                        shuffle=False)

    mean = 0.
    std = 0.
    for images, _ in loader:
        batch_samples = images.size(0) # batch size (the last batch can have smaller size!)
        images = images.view(batch_samples, images.size(1), -1)
        mean += images.mean(2).sum(0)
        std += images.std(2).sum(0)

    mean /= len(loader.dataset)
    std /= len(loader.dataset)
    print(f"Mean is: {mean}")
    print(f"Std is: {std}")