# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Qwen3 600M language model continual pretraining"""

import torch
from lightning.pytorch.loggers import TensorBoardLogger
from megatron.core.distributed import DistributedDataParallelConfig
from megatron.core.optimizer import OptimizerConfig
from nemo import lightning as nl
from nemo.collections import llm
from nemo.collections.llm.gpt.model.qwen3 import Qwen3Config600M, Qwen3Model
from nemo.lightning.pytorch.optim import MegatronOptimizerModule, WarmupAnnealingScheduler
from nemo.collections.llm.gpt.data import PreTrainingDataModule
from nemo.collections.nlp.modules.common.tokenizer_utils import get_nmt_tokenizer
from nemo.utils.exp_manager import TimingCallback
from lightning.pytorch.loggers import WandbLogger
import nemo_run as run

def main():
    """Entrypoint for continual pretraining"""

    training_steps = 60_000  # Set based on your dataset size and training needs

    tokenizer = get_nmt_tokenizer(
    library="huggingface",
    model_name="/home/training/qwen3-600m/context/nemo_tokenizer",
    )

    data = PreTrainingDataModule(
    paths=[
        # paths here
    ],
    seq_length=2048,
    micro_batch_size=10,
    num_workers=0,
    global_batch_size=2560,
    split="98,1,1",
    tokenizer=tokenizer
    )
    
    # Model configuration for Qwen3 600M
    model_config = Qwen3Config600M()
    model = Qwen3Model(model_config)
    
    # Strategy configuration optimized for continual pretraining
    strategy = nl.MegatronStrategy(
        tensor_model_parallel_size=1,
        pipeline_model_parallel_size=1,
        pipeline_dtype=torch.bfloat16,
        virtual_pipeline_model_parallel_size=None,
        context_parallel_size=1,
        expert_model_parallel_size=1,
        sequence_parallel=False,
        gradient_as_bucket_view=True,
        ckpt_async_save=True,
        ckpt_parallel_save=True,
        ckpt_parallel_load=True,
        ckpt_parallel_save_optim=True,
        ckpt_load_strictness="log_all",
        ddp=DistributedDataParallelConfig( 
            check_for_nan_in_grad=True,
            grad_reduce_in_fp32=True,
            overlap_grad_reduce=True,
            overlap_param_gather=True,
            average_in_collective=True,
        ),
    )
    
    # Trainer configuration
    trainer = nl.Trainer(
        accelerator="gpu",
        devices=8,
        num_nodes=4,
        max_steps=training_steps,  # Adjust based on your dataset size
        limit_val_batches=50,
        val_check_interval=2500,
        log_every_n_steps=10,
        strategy=strategy,
        accumulate_grad_batches=1,
        use_distributed_sampler=True,
        plugins=nl.MegatronMixedPrecision(precision="bf16-mixed"),
        enable_checkpointing=True,
        callbacks=[
            TimingCallback(),
        ],
    )
    
    opt_config = OptimizerConfig(
        optimizer="adam",
        lr=2e-5,
        weight_decay=0.01,
        bf16=True,
        fp16=False,
        adam_beta1=0.95, 
        adam_beta2=0.95,
        adam_eps=1e-5,
        use_distributed_optimizer=True,
        clip_grad=1.0,
    )
    
    # Learning rate scheduler for continual pretraining
    lr_scheduler = WarmupAnnealingScheduler(
        warmup_steps = 6000,
        max_steps=training_steps,
        min_lr=0,           # Minimum LR to avoid too low values
        )

    
    opt = MegatronOptimizerModule(config=opt_config, lr_scheduler=lr_scheduler)
    
    # Checkpoint configuration
    ckpt = nl.ModelCheckpoint(
        save_top_k=10,
        save_last=True,
        save_optim_on_train_end=True,
        filename="{step}-{consumed_samples}",
        every_n_train_steps=5000,
    )
    
    # Logger configuration
    tb = TensorBoardLogger(
        save_dir="tensorboard",
        name="qwen3_600m_continual",
    )

    wandb_logger = WandbLogger( 
        project="translation-expts",  # Name of the W&B project
        # project="qwen3-600M-ablation-exp-test",  # Name of the W&B project
        name="qwen3-ablation-exp",  # Name of this specific run
    )
    
    logger = nl.NeMoLogger(
        wandb=wandb_logger,
        explicit_log_dir="/home/training/qwen3_600m_continual",
        log_global_rank_0_only=True,
        update_logger_directory=True,
        ckpt=ckpt,
        tensorboard=tb,
    )
    
    # Resume configuration for continual pretraining
    # This loads the pretrained Qwen3 600M checkpoint
    resume = nl.AutoResume(
        restore_config=run.Config(
            nl.RestoreConfig,
            path="/home/training/qwen3-600m"  # Use the imported checkpoint
        ),
        resume_if_exists=True,
        resume_ignore_no_checkpoint=False,  # Ensure checkpoint exists
    )
    
    # Start continual pretraining
    llm.pretrain(
        model=model,
        data=data,
        trainer=trainer,
        log=logger,
        resume=resume,
        optim=opt,
    )

if __name__ == "__main__":
    main()
