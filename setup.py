import os.path as osp
from setuptools import setup, find_packages

# Defer torch import to avoid import errors during wheel building
def get_extensions():
    try:
        from torch.utils.cpp_extension import BuildExtension, CUDAExtension
    except ImportError:
        raise ImportError("PyTorch is required to build DPVO. Please install PyTorch first.")
    
    ROOT = osp.dirname(osp.abspath(__file__))
    
    return [
        CUDAExtension('cuda_corr',
            sources=['dpvo/altcorr/correlation.cpp', 'dpvo/altcorr/correlation_kernel.cu'],
            extra_compile_args={
                'cxx':  ['-O3'], 
                'nvcc': ['-O3'],
            }),
        CUDAExtension('cuda_ba',
            sources=['dpvo/fastba/ba.cpp', 'dpvo/fastba/ba_cuda.cu', 'dpvo/fastba/block_e.cu'],
            extra_compile_args={
                'cxx':  ['-O3'], 
                'nvcc': ['-O3'],
            },
            include_dirs=[
                osp.join(ROOT, 'thirdparty/eigen-3.4.0')]
            ),
        CUDAExtension('lietorch_backends', 
            include_dirs=[
                osp.join(ROOT, 'dpvo/lietorch/include'), 
                osp.join(ROOT, 'thirdparty/eigen-3.4.0')],
            sources=[
                'dpvo/lietorch/src/lietorch.cpp', 
                'dpvo/lietorch/src/lietorch_gpu.cu',
                'dpvo/lietorch/src/lietorch_cpu.cpp'],
            extra_compile_args={'cxx': ['-O3'], 'nvcc': ['-O3'],}),
    ]

def get_build_ext():
    try:
        from torch.utils.cpp_extension import BuildExtension
    except ImportError:
        raise ImportError("PyTorch is required to build DPVO. Please install PyTorch first.")
    return BuildExtension

ROOT = osp.dirname(osp.abspath(__file__))



setup(
    name='dpvo',
    packages=find_packages(),
    ext_modules=get_extensions(),
    cmdclass={
        'build_ext': get_build_ext()
    })

