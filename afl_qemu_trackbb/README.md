# get coverage from qemu to afl

when qemu simulate a program(bin/kernel/firmware...),
it use `struct TranslationBlock`(`include/exec/exec-all.h`) to refer the basic block,
and the field `target_ulong pc` simulated PC corresponding to this block (EIP + CS base), which can be use for code coverage, too.

in afl, it will covert into bb2bb coverage.
here we call it afl-style coverage.

these code will make a bridge between coverage user(eg. afl) and qemu
1. qemu: track pc of a basic block
2. qemu: write bb2bb(with prev pc) into share memory
3. user: read coverage info from share memory


# Usage

just work in Linux, testing ubuntu 16.04

## Qemu

[afl-qemu-cpu-inl.h](afl-qemu-cpu-inl.h) provide a marco `AFL_QEMU_CPU_SNIPPET2` for qemu to write bb pc in shm,
so when qemu execute a TranslationBlock, use `AFL_QEMU_CPU_SNIPPET2`!

in detail, in file `accel/tcg/cpu-exec.c`,
the function of `static inline tcg_target_ulong cpu_tb_exec(CPUState *cpu, TranslationBlock *itb)` is
Execute a TB, and fix up the CPU state afterwards if necessary.

so we modify code as follow:

```c
// in accel/tcg/cpu-exec.c
// ... some headers ...
#include "/path/to/afl-qemu-cpu-inl.h"
// ... other headers ...

// ...

static inline tcg_target_ulong cpu_tb_exec(CPUState *cpu, TranslationBlock *itb)
{
  CPUArchState *env = cpu->env_ptr;
  uintptr_t ret;
  TranslationBlock *last_tb;
  int tb_exit;
  uint8_t *tb_ptr = itb->tc.ptr;

  // patch here!!!
  AFL_QEMU_CPU_SNIPPET2(itb->pc);
  // patch end

  qemu_log_mask_and_addr(CPU_LOG_EXEC, itb->pc,
                          "Trace %d: %p ["
                          TARGET_FMT_lx "/" TARGET_FMT_lx "/%#x] %s\n",
                          cpu->cpu_index, itb->tc.ptr,
                          itb->cs_base, itb->pc, itb->flags,
                          lookup_symbol(itb->pc));

  //...
}

// ...
```

## Coverage User

in [QemuInterface.c](QemuInterface.c),
we provide 3 interfaces to access share memory which store afl-style coverage:
1. `int hit_new_bits(void);`
2. `int get_bitmap_size(void);`
3. `int get_current_cksum(void);`

it is easy to know what they do.

***bugfix:***

`hit_new_bits()` is error!!!

unless call `hit_new_bits()` or update `pre_cksum` after executing every basic block(TranslationBlock).

the root of error is this interface determine whether is hit_new_bits by determining if `pre_cksum != cur_cksum`, and `pre_cksum` just update in `hit_new_bits()`.

There are many ways to use QemuInterface.c, like:
1. split QemuInterface.c into declaration(.h) and definition(.c), and put them into user workplace, remember to fix compile rule for them.
2. [build.sh](build.sh) comile QemuInterface.c into QemuInterface.so, and use QemuInterface like use share lib, refer `dlsym()`, `dlopen()`, `dlclose()` in `#include <dlfcn.h>`.


## shm_id.txt

***important***

shm_id.txt store share memory id, it's better change absolute path(hard code) in [afl-qemu-cpu-inl.h](afl-qemu-cpu-inl.h) and [QemuInterface.c](QemuInterface.c)

# implementation
1. files in directory [afl](afl/) is come from project [AFL](https://github.com/google/AFL)
2. share memory open with [afl-qemu-cpu-inl.h](afl-qemu-cpu-inl.h), size define in [afl/config.h](afl/config.h), but no one close it, we can use [rmshm.sh](rmshm.sh) to close it.
3. origin author is not me, [guanle](https://github.com/guanleustc), [situ lingyun](https://github.com/stuartly), and maybe have others to coding it, I just fix some bugs, and make backup for me.
